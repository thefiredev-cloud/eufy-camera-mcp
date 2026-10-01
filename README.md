# eufy-cam-mcp

## What it is

A Python FastMCP server that exposes an allowlisted set of local Eufy cameras (snapshots, status, motion clips) through MediaMTX on localhost.

## Why it exists

Agents need camera status and a single JPEG without talking to unknown camera names, hitting the network except MediaMTX, or driving PTZ.

## How to run it

Runtime: Python >= 3.12, [uv](https://docs.astral.sh/uv/), lockfile `uv.lock`. Entry point: `eufy-cam-mcp` → `eufy_cam_mcp.server:main`.

```bash
uv sync --frozen
uv run eufy-cam-mcp
```

That starts the MCP stdio server. It expects MediaMTX at `http://127.0.0.1:9997` (API) and `rtsp://127.0.0.1:8554/<name>` (ffmpeg snapshots). Known names are hard-coded: `eufy_cam1`, `eufy_cam2`, `eufy_cam3`, `eufy_cam4`. Snapshots write under `~/meshvault/camera/snapshots`; recordings are read from `~/meshvault/camera/recordings`.

You supply the camera side: a MediaMTX instance that publishes your cameras under those four path names, and `ffmpeg` on `PATH`. The recorder that writes the `<name>_*.mp4` segments read by `recordings_info`, `motion_clips` and `clip_frame` is not part of this repository. To use other camera names, edit `KNOWN_CAMS` in `src/eufy_cam_mcp/server.py`.

If MediaMTX is not up, the documented no-camera happy path is the allowlist check (no network, no ffmpeg):

```bash
uv sync --frozen
uv run python scripts/check-camera-boundaries.py
```

Tools in `src/eufy_cam_mcp/server.py`: `list_cameras`, `camera_status`, `snapshot_camera`, `recordings_info`, `motion_clips`, `clip_frame`.

## In scope / out of scope

In scope:

- Allowlisted camera names only.
- Ready-state from MediaMTX `/v3/paths/list`.
- One-frame ffmpeg JPEG from local RTSP.
- Listing local `*.mp4` motion segments and extracting one frame from a named clip.

Out of scope:

- PTZ, talkback, cloud Eufy APIs, or cameras outside `eufy_cam1`–`eufy_cam4`.
- Recording or retention (that belongs to the recorder service; this server only reports files on disk).
- Path traversal camera names (`../../outside` and similar are rejected before API or ffmpeg).

## Current production URL

Not deployed.

## Status

live
