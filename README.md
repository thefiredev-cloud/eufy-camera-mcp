# eufy-camera-mcp

[![CI](https://github.com/thefiredev-cloud/eufy-camera-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/thefiredev-cloud/eufy-camera-mcp/actions/workflows/ci.yml)

A Python [FastMCP](https://gofastmcp.com) server that gives an AI agent view-only access to an allowlisted set of local Eufy cameras through [MediaMTX](https://github.com/bluenviron/mediamtx): live status, a single JPEG snapshot, and recorded motion clips. It has no PTZ, no talkback, and no cloud API.

## Why it exists

An agent that can see a camera should not be able to reach cameras it was not given, call out to the internet, or move the camera. This server keeps the surface small: four known camera names, localhost MediaMTX only, and one frame at a time.

## Tools

| Tool | What it returns |
|---|---|
| `list_cameras` | Each known camera with its ready state from MediaMTX |
| `camera_status` | Ready state, tracks, and error counters for one camera |
| `snapshot_camera` | Path to one JPEG frame grabbed with `ffmpeg` from local RTSP, plus a `<name>_latest.jpg` link |
| `recordings_info` | Segment count, disk use, and oldest and newest recording |
| `motion_clips` | Newest motion recordings for one camera, `limit` between 1 and 50 |
| `clip_frame` | Path to one JPEG frame at `t` seconds into a named clip in the recordings folder |

Every per-camera tool rejects names outside the allowlist, including path traversal attempts such as `../../outside`, before any MediaMTX call or `ffmpeg` process. `clip_frame` also rejects clip names that are not a bare `*.mp4` file name.

## Requirements

- Python 3.12 or newer and [uv](https://docs.astral.sh/uv/)
- `ffmpeg` on `PATH`
- A MediaMTX instance on the same host that publishes your cameras as `eufy_cam1` to `eufy_cam4`
- A recorder that writes `<name>_*.mp4` segments, if you want the recording tools (not part of this repo)

## Install and run

```bash
git clone https://github.com/thefiredev-cloud/eufy-camera-mcp.git
cd eufy-camera-mcp
uv sync --frozen
uv run eufy-cam-mcp
```

This starts the MCP server on stdio. Register it with your MCP client as a stdio command, for example:

```json
{
  "mcpServers": {
    "eufy-cam": {
      "command": "uv",
      "args": ["--directory", "/path/to/eufy-camera-mcp", "run", "eufy-cam-mcp"]
    }
  }
}
```

## Configuration

Settings are constants at the top of `src/eufy_cam_mcp/server.py`:

| Constant | Default |
|---|---|
| `MEDIA_MTX_API` | `http://127.0.0.1:9997` |
| `MEDIA_MTX_RTSP` | `rtsp://127.0.0.1:8554` |
| `KNOWN_CAMS` | `eufy_cam1`, `eufy_cam2`, `eufy_cam3`, `eufy_cam4` |
| `SNAP_DIR` | `~/meshvault/camera/snapshots` (snapshots are written here) |
| `REC_DIR` | `~/meshvault/camera/recordings` (recordings are read from here) |

The `~/meshvault/...` folders are the defaults used on the author's machines. Edit the constants to match your layout; there are no environment variable overrides yet.

## Check it without cameras

The boundary check calls `camera_status` and `snapshot_camera` with bad camera names and confirms that no MediaMTX call, network connection, `ffmpeg` process, or snapshot folder was created:

```bash
uv run python scripts/check-camera-boundaries.py
uv run pytest -v
```

CI runs Ruff, the boundary check, and the test suite on pushes and pull requests to `main`.

## Scope

In scope: allowlisted names, MediaMTX ready state from `/v3/paths/list`, one-frame JPEG capture, and listing and sampling local motion clips.

Out of scope: PTZ, talkback, Eufy cloud APIs, recording, and retention. Recording belongs to a separate recorder service; this server only reports files already on disk.

## Status

Working, version 0.1.0. Not published to PyPI and not deployed as a hosted service.

## License

MIT. See [LICENSE](LICENSE).
