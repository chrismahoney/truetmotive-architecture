# TrueMotive Architecture

The shared vocabulary for running TrueMotive: what an instance is, how people reach it, and what the pieces are called. Terms only; how things are built lives in [system/](system/) and the decisions in [adr/](adr/).

## Where it runs

**Instance**:
One complete, self-contained copy of the TrueMotive stack on exactly one physical host, with its own front door, proxy, database and containers. Nothing is shared between instances.
_Avoid_: Deployment, environment (that is the role an instance plays), server

**Environment**:
The role an instance plays: `dev`, `test` or `prod`. Each environment is one instance.
_Avoid_: Stage, tier

**Host**:
The physical or virtual machine an instance runs on. Hosts are named on the tailnet (`mahoney-mac`, `helpy`, `turbo-1`).
_Avoid_: Node, box

**Tailnet**:
The private Tailscale network (`mastodon-adder.ts.net`) that all people and hosts reach each other over. Being on it is the base access check.

**Clean room**:
A throwaway copy of the stack on a host, under its own compose project name and state folder, used to test without touching the real instance.
_Avoid_: Sandbox, staging

## How people get in

**Front door**:
The single `tailscale serve` entry on a host. It ends TLS with the host's tailnet certificate and hands plain HTTP to the proxy on loopback. An instance has exactly one.
_Avoid_: Gateway, ingress, funnel

**Tailnet identity**:
The `Tailscale-User-Login` and `Tailscale-User-Name` headers that the front door adds so downstream services know who the visitor is.

**Proxy**:
Nginx Proxy Manager (NPM) on a host. It receives everything from the front door and routes by path to the right container. It is the only thing that talks to the front door.
_Avoid_: Reverse proxy (too generic), Caddy (retired)

**Location**:
One path-prefix routing rule inside the proxy, such as `/` or `/tv/`.
_Avoid_: Route, host entry (hostnames are not used for routing)

**Proxy secret**:
A shared value (`TMD_PROXY_SECRET`) that the proxy sends with every request to TrueMotive's proxy listener. It proves the identity headers came from the proxy and not from another container.

## TrueMotive Desktop

**TMD**:
TrueMotive Desktop running as a web container. Users, orgs and events live in Postgres ("session mode").
_Avoid_: truemotive-desktop (that is the repository name)

**Main listener**:
TMD's own internal port. In session mode it must be bound to loopback inside the container, and it is only used by the container's healthcheck.

**Token listener**:
The TMD port that accepts a bearer token and nothing else. Used by scripts on the host.

**Proxy listener**:
The TMD port that trusts tailnet identity headers, but only when they arrive with the proxy secret. It is the port the proxy sends people to.

## Media

**MediaMesh**:
The repository and stack that runs everything in an instance: TMD, the engine, media services and their data.

**Engine**:
The container that runs channel graphs in Liquidsoap and serves the control API and HLS output.

**Channel**:
A running graph of inputs and outputs built in the Builder and compiled to Liquidsoap.

**Primary stack**:
The services in `docker-compose.yml`. The secondary stack (`docker-compose.secondary.yml`) holds older components kept for rollback.

## Operating

**Overlay**:
An extra compose file layered onto `docker-compose.yml` to change one concern, for example the `edge` overlay that adds the proxy.

**Punch list**:
The matrix of checks that must pass on every instance before it counts as working. See [punch-list/MATRIX.md](punch-list/MATRIX.md).

**Check**:
One row of the punch list: a single observable fact with a command that proves it.
