"""Vercel Python Function exposing a live PyEngine demo API."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

from pyengine.demo import build_demo_payload


class handler(BaseHTTPRequestHandler):
    """Serve deterministic engine state from a Vercel serverless function."""

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        frames = _parse_frames(query.get("frames", ["12"])[0])
        payload = build_demo_payload(frames)

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "s-maxage=60, stale-while-revalidate=300")
        self.end_headers()
        self.wfile.write(json.dumps(payload, indent=2).encode("utf-8"))


def _parse_frames(value: str) -> int:
    frames = int(value)
    if frames < 0 or frames > 240:
        raise ValueError("frames must be between 0 and 240")
    return frames
