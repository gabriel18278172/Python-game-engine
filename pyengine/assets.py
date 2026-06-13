"""Safe asset loading and caching."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, TypeVar

T = TypeVar("T")


class AssetManager:
    """Caches assets loaded from a configured root directory."""

    def __init__(self, root: str | Path = "assets") -> None:
        self.root = Path(root)
        self._cache: dict[str, object] = {}

    def path_for(self, relative_path: str | Path) -> Path:
        path = (self.root / relative_path).resolve()
        root = self.root.resolve()
        if root not in (path, *path.parents):
            raise ValueError("asset path escapes the asset root")
        return path

    def load_text(self, relative_path: str | Path, encoding: str = "utf-8") -> str:
        key = f"text:{relative_path}"
        if key not in self._cache:
            self._cache[key] = self.path_for(relative_path).read_text(encoding=encoding)
        return str(self._cache[key])

    def load(self, key: str, loader: Callable[[], T]) -> T:
        if key not in self._cache:
            self._cache[key] = loader()
        return self._cache[key]  # type: ignore[return-value]
