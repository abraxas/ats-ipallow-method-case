FROM ats-10.2.0-lab:local

USER root
COPY configs/remap.config /opt/ats/etc/trafficserver/remap.config
COPY configs/ip_allow.yaml /opt/ats/etc/trafficserver/ip_allow.yaml
COPY configs/records.yaml /opt/ats/etc/trafficserver/records.yaml
COPY configs/plugin.config /opt/ats/etc/trafficserver/plugin.config
COPY configs/storage.config /opt/ats/etc/trafficserver/storage.config
RUN mkdir -p /opt/ats/var/trafficserver /opt/ats/var/log/trafficserver \
 && chown -R nobody:nogroup /opt/ats/var \
 && /opt/ats/bin/traffic_server --version

EXPOSE 8080
CMD ["traffic_server"]
