# helpy build log

Host: Raspberry Pi 5 (arm64). Role: test. Tailnet name `helpy.mastodon-adder.ts.net`.
Status key: **reported** = stated by Chris, not checked on the host. **verified** = checked on the host.

## 2026-11-24

| # | Step | Status | Notes |
|---|---|---|---|
| 1 | Clean install of Ubuntu 26 LTS | reported | TODO: exact release (`/etc/os-release`), image, how it was flashed, boot media (SD or NVMe), Pi firmware/EEPROM version |
| 2 | Install Docker Engine | reported | Followed https://readthemanual.co.uk/pi5-docker-host/. TODO: which method (convenience script or Docker apt repo), `docker --version`, `docker compose version`, `docker run hello-world` result |
| 3 | Add `chris` to the `docker` group | reported | Needs a full log out and back in before it applies. The group is effectively root; say so in the guide |
| 4 | Join the tailnet | not done | Tailnet listed helpy offline (last seen about 23 h) and `tailscale ping helpy` timed out at 16:37. TRU-21 |
| 5 | SSH access from the Mac | not done | No identities loaded in the Mac's agent; key for the rebuilt host unconfirmed |

## Gaps in the source walkthrough

It is a Docker-foundations guide. It does not cover firmware/EEPROM, NVMe boot, static networking, `daemon.json` or daemon hardening. Its own advice worth keeping: pin image tags, publish only needed ports, `restart: unless-stopped`, check images for `linux/arm64`.

## Changes to earlier plans

The old helpy page assumed an existing Nginx Proxy Manager stack and a `docker-compose.helpy.yml` overlay to retire. A clean install removes both, so the build is greenfield. Open question: did anything in the old NPM need exporting first? Ask Chris.
