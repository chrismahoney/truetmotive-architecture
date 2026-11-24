# Adjacent services

Things that run on the same hosts but are not part of the TrueMotive stack. They are documented so nobody breaks them by accident. None is in the acceptance criteria and **nothing here is changed without a separate go-ahead**.

Status: observed on turbo-1 on 2026-11-24 ✅. Owners and purposes ❓ until you confirm.

| Item | Host | Observed | Notes | Owner / decision |
|---|---|---|---|---|
| `code-server` | turbo-1 | published `0.0.0.0:8443` | Browser IDE | ❓ keep, tailnet-only? |
| `metube` | turbo-1 | published `0.0.0.0:6968` | Video downloader | ❓ |
| `portainer` | turbo-1 | `8000`, `9443` on `0.0.0.0` | Docker UI | ❓ keep, tailnet-only? |
| `me2be_default` network | turbo-1 | exists | Unknown project | ❓ |
| `raspberrypi-docker_rpimonitor_default` network | turbo-1 | exists | Pi monitoring leftovers | ❓ |
| `caddy-stack_truemotive-core`, `tm-caddy_default`, `tm-caddy_portainer_network`, `truemotive-core` networks | turbo-1 | exist, no Caddy container running | Stale since Caddy was retired | to remove after confirmation |
| Other tailnet machines | tailnet | `aperture`, `gamepi`, `laser`, `truemotive`, `truemotive-dev`, `tailscale-nginx`, `dannys-mac-mini`, … | Not touched | ❓ which are still in use |
| Cloudflare and DNS | account | not audited | Used earlier for DNS-01 certificates; no longer needed under ADR 0002 | ⬜ |
| Jira tickets | `mediamesh/jira/` | JIRA-029 references the helpy overlay | ⬜ |

When one of these is put behind the front door later, it gets a path in the [path map](01-edge-and-identity.md#path-map-proposed-every-row-must-be-proven-on-each-host), not a new door.
