"""Unit tests for new eufy-cam MCP tools: motion clips and boundary behavior."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastmcp import Client

from eufy_cam_mcp import server


@pytest.fixture
def cam_dirs(tmp_path, monkeypatch):
    rec = tmp_path / "recordings"
    snap = tmp_path / "snapshots"
    rec.mkdir(parents=True)
    monkeypatch.setattr(server, "REC_DIR", rec)
    monkeypatch.setattr(server, "SNAP_DIR", snap)
    return rec, snap


@pytest.fixture
def client_factory(cam_dirs):
    async def _call(tool, args):
        async with Client(server.mcp) as client:
            res = await client.call_tool(tool, {"name": args} if False else args)
            return json.loads(res.data) if isinstance(res.data, (str, bytes)) else res.data
    return _call


import asyncio


def call_tool(args, tool):
    return asyncio_run(client_call(tool, args))


async def client_call(tool, args):
    async with Client(server.mcp) as client:
        res = await client.call_tool(tool, args)
        return res.data


def asyncio_run(coro):
    return asyncio.run(coro)


def test_motion_clips_unknown_camera_is_rejected(cam_dirs):
    out = asyncio_run(client_call("motion_clips", {"name": "nope", "limit": 3}))
    assert out["error"] == "unknown camera"


def test_motion_clips_lists_newest_segments(cam_dirs, tmp_path):
    rec, _ = cam_dirs
    for i, name in enumerate(["eufy_cam2_a.mp4", "eufy_cam2_b.mp4", "eufy_cam2_c.mp4"]):
        f = rec / name
        f.write_bytes(b"x")
        import os
        os.utime(f, (1000 + i, 1000 + i))
    out = asyncio_run(client_call("motion_clips", {"name": "eufy_cam2", "limit": 2}))
    # newest-first per the tool contract: c (mtime 1002) then b (1001); a (1000) is cut by limit
    assert [Path(p).name for p in out["clips"]] == ["eufy_cam2_c.mp4", "eufy_cam2_b.mp4"]
    assert out["count"] == 2


def test_clip_frame_rejects_unknown_camera(cam_dirs, monkeypatch):
    ran = []
    monkeypatch.setattr(server.subprocess, "run", lambda *a, **k: ran.append(a))
    out = asyncio_run(client_call("clip_frame", {"name": "../evil", "clip": "a.mp4", "t": 5}))
    assert out["error"] == "unknown camera"
    assert ran == []


def test_clip_frame_rejects_missing_clip(cam_dirs, monkeypatch):
    monkeypatch.setattr(server.subprocess, "run", lambda *a, **k: (_ for _ in ()).throw(AssertionError("ffmpeg ran")))
    out = asyncio_run(client_call("clip_frame", {"name": "eufy_cam1", "clip": "missing.mp4", "t": 5}))
    assert out["error"] == "clip not found"


def test_clip_frame_rejects_path_escape(cam_dirs, monkeypatch):
    rec, _ = cam_dirs
    (rec / "a.mp4").write_bytes(b"x")
    monkeypatch.setattr(server.subprocess, "run", lambda *a, **k: (_ for _ in ()).throw(AssertionError("ffmpeg ran")))
    out = asyncio_run(client_call("clip_frame", {"name": "eufy_cam1", "clip": "../../etc/passwd", "t": 5}))
    assert out["error"] in ("clip not found", "invalid clip name")
