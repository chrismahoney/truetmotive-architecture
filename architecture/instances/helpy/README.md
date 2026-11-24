# helpy — test

Raspberry Pi 5 (Linux, arm64). Tailnet name `helpy.mastodon-adder.ts.net`, tailnet IP `100.78.7.46`. **Not audited**: on 2026-11-24 `ssh chris@helpy` timed out and the tailnet listed it offline since about 7 hours earlier.

> **2026-11-24 update:** helpy was wiped and reinstalled (Ubuntu 26 LTS, clean install, Docker added). Everything below that mentions the old `nginxpm/` stack or `docker-compose.helpy.yml` is historical; the build is now greenfield. Build log and guide source: [install/helpy-build-log.md](../../install/helpy-build-log.md). Tasks: TRU-21 to TRU-28.

Acceptance: every required row in the [punch list](../../punch-list/MATRIX.md), column helpy. Third in order.

## What the repo says (🟡, unverified)

- Nginx Proxy Manager runs here from a separate `nginxpm/` stack on 80/443, with an external Docker network named `truemotive`.
- `docker-compose.helpy.yml` attached `truemotive`, `web` and `spacecom` to that network and published no port for `occc-ui`.
- That overlay is replaced by the `edge` overlay ([ADR 0005](../../adr/0005-nginx-proxy-manager-as-an-in-repo-edge-overlay.md)).

## Open questions (❓)

1. Why is it offline: power, network, or SD/NVMe? Needs a physical or console check.
2. Does the existing NPM here hold proxy hosts worth exporting before it is replaced?
3. Does the full stack fit on a Pi 5 (arm64 images for every service, `rist-receiver-dante` build, LiveKit)? If not, which services are omitted in `test`?
4. Is its current checkout and TMD version known? Not until it is reachable.

## What can be answered without the Pi (checked 2026-11-24)

Open question 3 is mostly settled by the registries. Every image the stack pulls or builds `FROM` publishes `linux/arm64`: `postgres:16-alpine`, `busybox:1.36`, `jc21/nginx-proxy-manager:2.16.0`, `ghcr.io/gethomepage/homepage:v2.7.0`, `ghcr.io/tecnativa/docker-socket-proxy:v0.4.1`, `livekit/livekit-server`, `bluenviron/mediamtx`, `savonet/liquidsoap:v2.4.5` (the engine), `node:22-alpine`, `alpine:3.21`, and the Playwright base. `engine/Dockerfile` already has an `arm64` branch for its Node download.

Still unknown, and only a build on the Pi will tell:

1. **The `sidecars/librist` source build** (used by `ristd`, `rist-receiver`, `rist-receiver-dante`) on arm64 Alpine.
2. **NDI.** The SDK is supplied in `data/ndi` and is a per-architecture download; the Pi needs the arm64 one, or NDI inputs are out of scope for `test`.
3. **Headroom.** 21 services including Playwright (browser capture, chopper renderer) and Liquidsoap encodes. Likely too much for a Pi 5 under real load. A reduced profile is the realistic `test` shape.

## Plan

Gated by physical or console access; nothing here has been run.

1. **Get it reachable.** Power, network, then storage (SD or NVMe). Confirm `tailscale status` shows `helpy` online and `ssh chris@helpy` works (the key is `~/.ssh/id_ed25519`, `IdentitiesOnly yes`; note `HostName helpy` relies on MagicDNS).
2. **Read-only snapshot before any change.** `docker ps`, `docker compose ls`, `git -C <checkout> status` and `describe`, `tailscale serve status`, free disk and RAM, and an export of the existing `nginxpm/` proxy hosts (open question 2). Store it under `~/pre-remediation-<date>/` on the Pi and log it as helpy A5, as was done on turbo-1.
3. **Decide the `test` shape (needs you).** Full stack, or a reduced profile: for example `truemotive`, `postgres`, `edge`, `web`, `occc-ui`, `engine`, `mediamtx`, `spacecom`, with `livekit`, `decisions`, `homepage`, the browser-capture tooling and the RIST Dante receiver left off. Whatever is omitted is written down on this page, so the missing rows are `➖` on purpose.
4. **Apply the same recipe as the other two hosts, in this order:** retire the old `nginxpm/` stack and the `docker-compose.helpy.yml` overlay, then the `edge` overlay, `tailscale serve --https=443` to `127.0.0.1:8880`, TMD at the pinned tag, then paths and exposure. The punch-list column for helpy already has every row.
5. **Prove it the same way:** valid certificate and tailnet identity from a peer, forged-header rejection, and the clean-room approach (`mmaudit`) is not needed again because the recipe is now proven on two hosts.

Risks to watch on this host in particular: the Pi runs the old NPM on `80`/`443` directly, so the cutover has a window with no front door; `/` on `helpy` is the only way back in if the tailnet path is the one that breaks, so keep the SSH session open and the LAN address handy during that step.
