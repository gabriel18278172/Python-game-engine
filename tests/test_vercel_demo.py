from pyengine.demo import build_demo_payload
from api.index import _parse_frames


def test_demo_payload_is_json_ready():
    payload = build_demo_payload(12)

    assert payload["engine"] == "PyEngine"
    assert payload["frames"] == 12
    assert payload["player_position"] == {"x": 7.0, "y": 2}
    assert "@@@@" in payload["frame"]


def test_vercel_frame_parser_bounds():
    assert _parse_frames("24") == 24
