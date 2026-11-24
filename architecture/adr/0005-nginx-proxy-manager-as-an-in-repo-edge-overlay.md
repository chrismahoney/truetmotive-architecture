---
status: accepted
---

# NPM is defined in the mediamesh repo as an `edge` overlay; Caddy is removed

The proxy is Nginx Proxy Manager, shipped as `docker-compose.edge.yml` with a compose-owned `edge` network, so the same file runs on all three hosts. It replaces the `caddy` service, `caddy/Caddyfile` and `docker-compose.helpy.yml`. We rejected keeping a separate NPM stack per host (helpy's `nginxpm/` with its external `truemotive` network) because that is how the hosts drifted apart. The NPM admin UI is loopback-only and reached with an SSH tunnel; its proxy-host configuration is exported to committed JSON, minus secrets, so a host can be rebuilt.
