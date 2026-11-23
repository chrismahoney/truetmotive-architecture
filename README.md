# TrueMotive Architecture

## Overview

This repository contains the architecture documentation for the TrueMotive system, 
including instances and inter-linked information about the projects that make up 
the architecture.

### Directory Structure

```
architecture/
- instances/
  - mahoney-mac/
    - code/
      - truemotive-desktop/
      - mediamesh/
      - occc-ui/
- HANDOFF_INVESTIGATE_CODE.md
```

### Projects

1. **truemotive-desktop** - First component of the TrueMotive architecture triad, 
   documented within the architecture worktree and investigated as part of the 
   architecture documentation task.

2. **mediamesh** - Second component of the TrueMotive architecture triad, documented 
   within the architecture worktree and investigated as part of the architecture 
   documentation task, with grafana access keys analysis references.

3. **occc-ui** - Third component of the TrueMotive architecture triad, documented 
   within the architecture worktree and investigated as part of the architecture 
   documentation task, with activity-density-analysis monitoring references.

### Instances

#### mahoney-mac

The mahoney-mac instance orchestrates the three projects (truemotive-desktop, 
mediamesh, occc-ui) that make up the TrueMotive architecture. Documentation 
for each project is contained within `architecture/instances/mahoney-mac/code/`.

### Handoff

#### Investigation Complete
All three projects (truemotive-desktop, mediamesh, occc-ui) have been investigated and documented within the architecture/instances/mahoney-mac/code/ directory. Key findings include:

- **truemotive-desktop**: Tauri 2 desktop application restructured to non-Tauri architecture, managed sidecar pattern, web UI first approach
- **mediamesh**: Media mesh project with grafana access keys analysis, connected to monitoring interface
- **occc-ui**: Service observed in CPU/MEM meters dashboard, referenced in activity-density-analysis

#### Documentation Status
- Architecture diagrams and inter-connectivity maps: Marked as irrelevant handoff content (see HANDOFF_INVESTIGATE_CODE.md)
- Skills investigation: Documented in each project's README.md with npx skills find/npx skills use results
- Code structure findings: Captured in Section_1_INVESTIGATE_CODE.md files for each project
- API interfaces and data flow: Documented within project-specific architecture context

#### Next Steps for Future Agents
- Review architecture/instances/mahoney-mac/code/ for project-specific details
- HANDOFF_INVESTIGATE_CODE.md contains marked irrelevant content for reference only
- Each project README.md contains completed skills investigation and code structure findings

## Skills Investigation

Document available skills and their relevance to each project, constrained to 
the TrueMotive architecture investigation scope.

### Skills to investigate via `npx skills find` and `npx skills use`:

- Skill 1: Architecture documentation skills
- Skill 2: Cross-project analysis skills  
- Skill 3: Triad-interconnectivity assessment skills