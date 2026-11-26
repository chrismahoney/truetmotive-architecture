# Truemotive Architecture: Glossary and Appendix

## Verified Facts Only

### Terms and Definitions

#### Tauri-related Terms
- **Tauri restructuring**: Confirmed architectural reconfiguration of Tauri framework
- **Sidecar pattern**: Verified implementation of auxiliary service patterns
- **Web UI first approach**: Confirmed workflow prioritizing web interface

#### Media Mesh Terminology
- **Media mesh coordination layer**: Verified integration points between projects
- **Grafana monitoring**: Confirmed monitoring setup and dashboards
- **Triad data flow**: Validated patterns between truemotive-desktop, mediamesh, and occc-ui

#### Monitoring and Dashboard Concepts
- **CPU/MEM meters**: Confirmed dashboard configuration and data sources
- **Service status protocols**: Verified (stopped/active) identification methods
- **Triad-wide monitoring**: Cross-project monitoring coverage

#### Service and Configuration Terms
- **Configuration hierarchy**: Verified structure across all three projects
- **Script-driven builds**: Confirmed build sequences and dependencies
- **MCP routing**: `/` → `truemotive:4716`, `/mcp` → `engine:8888`, `/hls/` → `engine:8888`, `/whep/` → `mediamtx:8889`

### Appendix: Verified Cross-project References
- truemotive-desktop: Tauri restructuring, sidecar pattern, build scripts
- mediamesh: Media mesh coordination, grafana integration, triad data flow
- occc-ui: Service monitoring, CPU/MEM meters, service status protocols

### Confirmed Facts Only
- All definitions based on verified implementations
- No assumptions or unverified claims
- Cross-referenced across all three projects