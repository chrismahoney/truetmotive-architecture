# TrueMotive architecture

How TrueMotive is put together and how to prove an instance works. Written so one person can explain the whole product, from the browser to the media ports.

**Status key used throughout:** ✅ verified on a real host · 🟡 documented from the repo, not yet proven live · ⬜ stub (exists, not yet written up) · ❓ unknown, needs an owner's answer.

## Start here

| If you want to… | Read |
|---|---|
| Understand the whole product in two minutes | [system/00-overview.md](system/00-overview.md) |
| Know how a visitor gets in and who TMD thinks they are | [system/01-edge-and-identity.md](system/01-edge-and-identity.md) |
| Know what each container does and which port it owns | [system/02-services.md](system/02-services.md) |
| See where state lives and what to back up | [system/03-data.md](system/03-data.md) |
| Follow audio and video from contributor to viewer | [system/04-media-plane.md](system/04-media-plane.md) |
| See how code becomes a running container | [system/05-build-and-deploy.md](system/05-build-and-deploy.md) |
| Operate, back up, debug | [system/06-operations.md](system/06-operations.md) |
| Know what else lives on these hosts | [system/07-adjacent-services.md](system/07-adjacent-services.md) |
| Compare dev, test and prod | [system/08-environments.md](system/08-environments.md) |
| Check whether an instance is done | [punch-list/MATRIX.md](punch-list/MATRIX.md) |
| Learn a term | [GLOSSARY.md](GLOSSARY.md) |
| See why a decision was made | [adr/](adr/) |
| Understand the 2026-11-24 outage | [remediation/TMD-RESTART-LOOP.md](remediation/TMD-RESTART-LOOP.md) |

## Environments

| Environment | Host | Tailnet name | Doc |
|---|---|---|---|
| dev | mahoney-mac | `mahoney-mac.mastodon-adder.ts.net` | [instances/mahoney-mac/](instances/mahoney-mac/) |
| test | helpy (Raspberry Pi 5) | `helpy.mastodon-adder.ts.net` | [instances/helpy/](instances/helpy/) |
| prod | turbo-1 | `turbo-1.mastodon-adder.ts.net` | [instances/turbo-1/](instances/turbo-1/) |

## Layout

```
architecture/
├── README.md              this index
├── GLOSSARY.md            vocabulary (terms only)
├── adr/                   decisions that are hard to reverse
├── system/                the product, layer by layer, with diagrams
├── instances/<host>/      what is true on each host
├── punch-list/            the acceptance matrix
└── remediation/           audit, patch and plan from 2026-11-24
```

## Writing rules for these docs

- Diagrams are Mermaid in fenced blocks, so they render on GitHub with no tooling.
- Every claim about a live host says where it was observed and when. If it was not observed, it is marked 🟡 or ❓.
- Secrets never appear here. Name the variable, never the value.
- A page that does not know something says so and lists who can answer, rather than guessing.
