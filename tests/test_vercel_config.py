import tomllib
from pathlib import Path


def test_vercel_entrypoint_is_explicit():
    config = tomllib.loads(Path("pyproject.toml").read_text())

    assert config["tool"]["vercel"]["entrypoint"] == "api/index.py"
    assert Path(config["tool"]["vercel"]["entrypoint"]).is_file()
