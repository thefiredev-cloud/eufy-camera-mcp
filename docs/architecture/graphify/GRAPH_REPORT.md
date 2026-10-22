# Graph Report - eufy-camera-mcp  (2026-10-21)

## Corpus Check
- 6 files · ~2,405 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 2, .lock 1)

## Summary
- 77 nodes · 125 edges · 12 communities (4 shown, 8 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 13 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- test_server_tools.py
- check-camera-boundaries.py
- Repository Guidelines
- eufy-camera-mcp
- server.py
- Tools
- client_factory
- clip_frame
- camera_status
- list_cameras
- snapshot_camera
- eufy-cam-mcp

## God Nodes (most connected - your core abstractions)
1. `client_call()` - 10 edges
2. `asyncio_run()` - 10 edges
3. `eufy-camera-mcp` - 10 edges
4. `Repository Guidelines` - 9 edges
5. `clip_frame()` - 8 edges
6. `camera_status()` - 7 edges
7. `Tools` - 7 edges
8. `list_cameras()` - 6 edges
9. `snapshot_camera()` - 6 edges
10. `motion_clips()` - 5 edges

## Surprising Connections (you probably didn't know these)
- `Tools` --references--> `list_cameras()`  [INFERRED]
  README.md → src/eufy_cam_mcp/server.py
- `Status` --references--> `camera_status()`  [INFERRED]
  README.md → src/eufy_cam_mcp/server.py
- `Tools` --references--> `camera_status()`  [INFERRED]
  README.md → src/eufy_cam_mcp/server.py
- `Check it without cameras` --references--> `snapshot_camera()`  [INFERRED]
  README.md → src/eufy_cam_mcp/server.py
- `Tools` --references--> `snapshot_camera()`  [INFERRED]
  README.md → src/eufy_cam_mcp/server.py

## Import Cycles
- None detected.

## Communities (12 total, 8 thin omitted)

### Community 0 - "test_server_tools.py"
Cohesion: 0.25
Nodes (11): asyncio_run(), call_tool(), client_call(), test_clip_frame_extracts_jpeg_from_synthetic_clip(), test_clip_frame_rejects_bad_t(), test_clip_frame_rejects_missing_clip(), test_clip_frame_rejects_other_cameras_clip(), test_clip_frame_rejects_path_escape() (+3 more)

### Community 2 - "Repository Guidelines"
Cohesion: 0.20
Nodes (9): Architecture & Data Flow, Code Conventions & Common Patterns, Development Commands, Important Files, Key Directories, Project Overview, Repository Guidelines, Runtime/Tooling Preferences (+1 more)

### Community 3 - "eufy-camera-mcp"
Cohesion: 0.25
Nodes (7): Configuration, eufy-camera-mcp, Install and run, License, Requirements, Scope, Why it exists

### Community 5 - "Tools"
Cohesion: 0.40
Nodes (3): Tools, motion_clips(), recordings_info()

## Knowledge Gaps
- **1 isolated node(s):** `eufy-cam-mcp`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 37 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `eufy-camera-mcp` connect `eufy-camera-mcp` to `camera_status`, `list_cameras`, `Tools`?**
  _High betweenness centrality (0.151) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `clip_frame()` (e.g. with `Check it without cameras` and `Status`) actually correct?**
  _`clip_frame()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `eufy-cam-mcp` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Why does `clip_frame()` connect `clip_frame` to `server.py`, `Tools`, `camera_status`, `list_cameras`, `snapshot_camera`?**
  _High betweenness centrality (0.106) - this node is a cross-community bridge._
- **Why does `Tools` connect `Tools` to `eufy-camera-mcp`, `clip_frame`, `camera_status`, `list_cameras`, `snapshot_camera`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._