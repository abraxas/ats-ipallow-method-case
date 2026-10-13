#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-ats-ipallow-method-case}"
export PYTHONUNBUFFERED=1

LABEL="ats-ipallow-method-case"
WITNESS="ATS-IPALLOW-METHOD-CASE-WITNESS"
IMAGE="ats-10.2.0-lab:local"
SRC_REL="../../client-reviews/trafficserver/src"
SRC_COPY="/tmp/ats-10.2.0-src"
LOCK="/tmp/ats-10.2.0-lab.lock"

down() {
  echo "== docker compose down -v =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" down -v --remove-orphans || true
}

trap down EXIT

fail_setup() {
  local reason="$1"
  echo "FAIL ${LABEL} ${reason} ${WITNESS}" | tee poc-last-run.txt
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=120 || true
  exit 1
}

ensure_ats_image() {
  # Portable exclusive lock (Linux flock(1) is missing on macOS hosts).
  python3 - "${LOCK}" "${IMAGE}" "${SRC_REL}" "${SRC_COPY}" <<'PY'
import fcntl
import os
import shutil
import subprocess
import sys

lock_path, image, src_rel, src_copy = sys.argv[1:5]
fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o644)
fcntl.flock(fd, fcntl.LOCK_EX)
inspect = subprocess.run(
    ["docker", "image", "inspect", image],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    check=False,
)
if inspect.returncode == 0:
    print(f"IOC shared-image-present {image}", flush=True)
    sys.exit(0)
print(f"== rsync ATS 10.2.0 source and build {image} ==", flush=True)
os.makedirs(src_copy, exist_ok=True)
subprocess.check_call(
    [
        "rsync",
        "-a",
        "--delete",
        "--exclude",
        ".git",
        "--exclude",
        "doc",
        "--exclude",
        "tests",
        "--exclude",
        "ci",
        src_rel.rstrip("/") + "/",
        src_copy.rstrip("/") + "/",
    ]
)
shutil.copyfile("Dockerfile.base", os.path.join(src_copy, "Dockerfile.base"))
subprocess.check_call(["docker", "build", "-t", image, "-f", "Dockerfile.base", src_copy])
subprocess.check_call(["docker", "image", "inspect", image], stdout=subprocess.DEVNULL)
PY
}

echo "== docker compose down (clean) =="
down
trap down EXIT

ensure_ats_image

echo "== docker compose up --build =="
up_ok=0
for attempt in $(seq 1 8); do
  if docker compose -p "${COMPOSE_PROJECT_NAME}" up -d --build; then
    up_ok=1
    break
  fi
  echo "IOC compose-up-retry attempt=${attempt}"
  sleep 8
  docker compose -p "${COMPOSE_PROJECT_NAME}" down -v --remove-orphans || true
done
if [[ "${up_ok}" != 1 ]]; then
  fail_setup "compose-up-failed"
fi

echo "== wait ATS 127.0.0.1:18710 GET / Host: ats.example =="
ready=0
for i in $(seq 1 90); do
  code="$(curl -sS -o /tmp/ats-ipallow-ready.txt -w '%{http_code}' --max-time 4 \
    -H 'Host: ats.example' 'http://127.0.0.1:18710/' || true)"
  body="$(tr -d '\r' </tmp/ats-ipallow-ready.txt 2>/dev/null || true)"
  if [[ "${code}" == "200" && "${body}" == *GET-OK* ]]; then
    ready=1
    echo "IOC ready attempt=${i} code=${code}"
    break
  fi
  echo "IOC wait attempt=${i} code=${code} body=${body:0:80}"
  sleep 2
done
if [[ "${ready}" != 1 ]]; then
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=160 || true
  fail_setup "not-ready"
fi

echo "== poc.py via attacker sidecar =="
set +e
docker compose -p "${COMPOSE_PROJECT_NAME}" exec -T attacker python3 /lab/poc.py | tee poc-last-run.txt
rc=${PIPESTATUS[0]}
set -e

if ! tail -n1 poc-last-run.txt 2>/dev/null | grep -qE '^(SUCCESS|FAIL) '; then
  echo "FAIL ${LABEL} poc-exit=${rc} ${WITNESS}" >> poc-last-run.txt
  rc=1
fi

exit "${rc}"
