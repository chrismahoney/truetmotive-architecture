---
status: accepted
---

# TMD trusts tailnet identity only on the proxy listener, and only with the proxy secret

TMD has three listeners. Only one of them reads `Tailscale-User-Login`, and it ignores that header unless `X-TMD-Proxy-Secret` matches `TMD_PROXY_SECRET`. The proxy sends the secret; nothing else on the Docker network knows it. This is why TMD must never be reachable by the proxy on any other port.

This ADR exists because misconfiguring these ports caused the 2026-11-24 restart loop: see [system/01-edge-and-identity.md](../system/01-edge-and-identity.md#tmd-has-three-listeners-and-they-must-not-overlap) for the table and the failure.

**Consequence.** The secret has to reach NPM without being committed. Plan: render an NPM `server_proxy.conf` snippet from `.env` at deploy time into a gitignored folder (see the open question in the edge page). Never paste the secret into an NPM config that is exported to git.
