"""Exercise the actual MCP input boundary without camera or filesystem writes."""
import asyncio
import json
import socket
import tempfile
from pathlib import Path
from unittest.mock import patch

from fastmcp import Client

from eufy_cam_mcp import server


async def main():
    with tempfile.TemporaryDirectory(prefix="camera-boundary-proof-") as root:
        snapshots = Path(root) / "snapshots"
        with (
            patch.object(server, "SNAP_DIR", snapshots),
            patch.object(server, "_api_paths", side_effect=AssertionError("Unexpected camera API access")) as api,
            patch.object(server.subprocess, "run", side_effect=AssertionError("Unexpected ffmpeg execution")) as process,
            patch.object(socket.socket, "connect", side_effect=AssertionError("Unexpected network connection")) as connect,
        ):
            checked = 0
            async with Client(server.mcp) as client:
                for name in ["../../outside", "/tmp/outside", "eufy_cam1/../outside", "unknown"]:
                    for tool in ["camera_status", "snapshot_camera"]:
                        result = await client.call_tool(tool, {"name": name})
                        assert "error" in result.data, result
                        checked += 1
            api.assert_not_called()
            process.assert_not_called()
            connect.assert_not_called()
            assert not snapshots.exists()
            print(json.dumps({
                "rejected_camera_calls": checked,
                "network_connections": connect.call_count,
                "ffmpeg_processes": process.call_count,
                "snapshot_directory_created": snapshots.exists(),
            }))


if __name__ == "__main__":
    asyncio.run(main())
