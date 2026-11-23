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

TODO: Add handoff investigation notes.

## Skills Investigation

Document available skills and their relevance to each project, constrained to 
the TrueMotive architecture investigation scope.

### Skills to investigate via `npx skills find` and `npx skills use`:

- Skill 1: Architecture documentation skills
- Skill 2: Cross-project analysis skills  
- Skill 3: Triad-interconnectivity assessment skills