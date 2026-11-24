# helpy — test

Raspberry Pi 5 (Linux, arm64). Tailnet name `helpy.mastodon-adder.ts.net`, tailnet IP `100.78.7.46`. **Not audited**: on 2026-11-24 `ssh chris@helpy` timed out and the tailnet listed it offline since about 7 hours earlier.

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

## Plan

Bring it back online, snapshot what is there (NPM export, `docker ps`, `git status`), then follow the same punch-list order as turbo-1.
