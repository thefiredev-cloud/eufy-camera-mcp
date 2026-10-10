# eufy-camera-mcp

[![CI](https://github.com/thefiredev-cloud/eufy-camera-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/thefiredev-cloud/eufy-camera-mcp/actions/workflows/ci.yml)

A Python [FastMCP](https://gofastmcp.com) server that gives an AI agent view-only access to an allowlisted set of local Eufy cameras through [MediaMTX](https://github.com/bluenviron/mediamtx): live status, a single JPEG snapshot, and recorded motion clips. It has no PTZ, no talkback, and no cloud API.

## Why it exists

An agent that can see a camera should not be able to reach cameras it was not given, call out to the internet, or move the camera. This server keeps the surface small: four known camera names, localhost MediaMTX only, and one frame at a time.

## Tools

The server registers six tools (`src/eufy_cam_mcp/server.py`).

| Tool | What it returns |
|---|---|
| `list_cameras` | Each known camera with its ready state and tracks from MediaMTX |
| `camera_status` | Ready state, tracks, received bytes, and inbound frames in error for one camera |
| `snapshot_camera` | Path to one JPEG frame grabbed with `ffmpeg` from local RTSP, plus a `<name>_latest.jpg` symlink to it |
| `recordings_info` | Segment count, total bytes, first and last file name in the recordings folder, and a fixed retention note |
| `motion_clips` | Paths of the newest `<name>_*.mp4` recordings for one camera by modification time, `limit` clamped to 1 to 50 |
| `clip_frame` | Path to one JPEG frame at `t` seconds into a named clip in the recordings folder |

Every per-camera tool rejects names outside the allowlist, including path traversal attempts such as `../../outside`, before any MediaMTX call or `ffmpeg` process. `clip_frame` also rejects clip names that are not a bare `*.mp4` file name, and returns `clip not found` for a name that does not exist in the recordings folder. It does not check that the clip file name starts with the camera name, and it does not range-check `t`.

`snapshot_camera` and `clip_frame` write JPEGs to the snapshot folder. Nothing deletes them. `recordings_info` sorts by file name, so with several cameras its first and last entries are alphabetical, not oldest and newest in time.

## Requirements

- Python 3.12 or newer and [uv](https://docs.astral.sh/uv/)
- `ffmpeg` on `PATH`
- A MediaMTX instance on the same host with its API enabled, publishing your cameras as `eufy_cam1` to `eufy_cam4`
- A recorder that writes `<name>_*.mp4` segments into the recordings folder, if you want the recording tools (not part of this repo)

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

The boundary check calls `camera_status` and `snapshot_camera` with four bad camera names and confirms that no MediaMTX call, network connection, `ffmpeg` process, or snapshot folder was created. The pytest suite has five tests: unknown camera rejection, newest-first clip listing, and `clip_frame` rejection of unknown cameras, missing clips, and path escapes.

```bash
uv run python scripts/check-camera-boundaries.py
uv run pytest -v
```

CI runs Ruff, the boundary check, and the test suite on pushes and pull requests to `main`.

## Scope

In scope: allowlisted names, MediaMTX ready state from `/v3/paths/list`, one-frame JPEG capture, and listing and sampling local motion clips.

Out of scope: PTZ, talkback, Eufy cloud APIs, recording, and retention. Recording belongs to a separate recorder service; this server only reads files already on disk.

## Status

Early, version 0.1.0. The tests and the boundary check cover input rejection and clip listing. No test runs `ffmpeg` capture, talks to MediaMTX, or uses a camera. If MediaMTX is unreachable, `list_cameras` and `camera_status` raise an error instead of returning a not-ready state. `ffmpeg` calls are limited to 60 seconds, and a timeout also raises. Not published to PyPI and not deployed as a hosted service.

## License

MIT. See [LICENSE](LICENSE).
