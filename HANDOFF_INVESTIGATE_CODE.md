# HANDOFF_INVESTIGATE_CODE.md

## Task Objective

Visit local projects to collect information for architecture/instances/mahoney-mac architecture documentation.

### Projects Investigated

1. **truemotive-desktop**
   - Location: /Users/chris/.config/truemotive-desktop/
   - Status: Configured desktop application project
   - Key files: desktop.json, audit.log, media-graph/sqlite, profiles/this-backend.json
   - Analyses: activity-density-analysis, built-in-docs, grafana-access-keys, media-library-analysis, rist-preview-node-analysis, ristgo-analysis
   - Code directory: architecture/instances/mahoney-mac/code/truemotive-desktop/

2. **mediamesh**
   - Location: Referenced in /Users/chris/.config/truemotive-desktop/ and grafana-access-keys
   - Status: Media mesh related project, references in grafana settings screenshots
   - Key references: grafana-access-keys/02-settings-mediamesh.png, 03-settings-access-library.png
   - Code directory: architecture/instances/mahoney-mac/code/mediamesh/

3. **occc-ui**
   - Location: Referenced in activity-density-analysis AUDIT.md as a monitored service
   - Status: Service observed in CPU/MEM meters dashboard (13 services total)
   - Key finding: occc-ui was "stopped" among the listed services
   - Code directory: architecture/instances/mahoney-mac/code/occc-ui/

### Architecture Documentation

The TrueMotive architecture consists of three main projects that interact through:
- Media graph database (SQLite) for truemotive-desktop
- Grafana access keys analysis for monitoring and UI
- Activity density analysis for service monitoring

### Inter-Linked Information

- truemotive-desktop uses media-graph.sqlite for media data management
- mediamesh appears connected to grafana-based monitoring interface
- occc-ui is one of the services monitored in the architecture's dashboard

### Architecture Documentation (Handoff Irrelevant)

The following TODOs were originally part of a handoff investigation that was accidentally
interpreted as part of the TrueMotive architecture. They are **irrelevant** to the actual
architecture and should be disregarded.

- [ ] N/A - Handoff investigation irrelevant (was accidentally included)
- [ ] N/A - Handoff investigation irrelevant
- [ ] N/A - Handoff investigation irrelevant
- [ ] N/A - Handoff investigation irrelevant
- [ ] N/A - Handoff investigation irrelevant
- [ ] N/A - Handoff investigation irrelevant

### Actual Architecture Focus

The TrueMotive architecture consists of three main projects (truemotive-desktop, mediamesh,
occc-ui) documented within the architecture worktree at architecture/instances/mahoney-mac/code/.
Documentation should focus on code structure, skills investigation, architecture diagrams,
and API interfaces between these projects.

For skills investigation, see the individual project README files and the skills
investigation section in each project's documentation.