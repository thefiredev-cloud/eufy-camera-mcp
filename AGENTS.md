# Repository Guidelines

## Project Overview

This Python FastMCP server exposes Eufy camera status, snapshots, and recordings through local MediaMTX. The configured camera allowlist is a security boundary.

## Architecture & Data Flow

`src/eufy_cam_mcp/server.py` registers camera tools and checks the allowlist before status lookup or snapshot work. Recording is handled by the recorder service; this MCP reads its local surfaces and does not establish recording retention by itself.

## Key Directories

- `src/eufy_cam_mcp/`: server and tool implementation.
- `tests/`: MCP tool tests.
- `scripts/check-camera-boundaries.py`: isolated hostile-name boundary check.
- `pyproject.toml`, `uv.lock`: Python 3.12+ dependencies and entry point.

## Development Commands

```bash
uv sync --frozen
uv run pytest
.venv/bin/python scripts/check-camera-boundaries.py
```

The boundary check forbids network connections and ffmpeg execution; it does not establish live camera availability, recording coverage, or effective retention.

## Code Conventions & Common Patterns

Enforce the allowlist before any camera work. Keep local MediaMTX paths and camera identifiers scoped to the configured set. Preserve fail-closed behavior for unknown or hostile camera names.

## Important Files

- `src/eufy_cam_mcp/server.py`: tool and allowlist boundary.
- `scripts/check-camera-boundaries.py`: isolated boundary verification.
- `README.md`: the limits of that verification and retention caveat.

## Runtime/Tooling Preferences

Use the project `uv.lock` and Python 3.12 or newer. Do not broaden camera access, export recordings, or expose private media without explicit authorization.

## Testing & QA

Run `uv run pytest` and the documented boundary check for relevant changes. These tests do not prove live camera health or recorder retention; check those through their own authorized runtime surfaces.
