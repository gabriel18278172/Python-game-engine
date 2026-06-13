"""Frame timing utilities."""

from __future__ import annotations

from time import perf_counter, sleep


class Clock:
    """Tracks delta time and optional frame-rate limiting."""

    def __init__(self, target_fps: int = 60) -> None:
        if target_fps <= 0:
            raise ValueError("target_fps must be positive")
        self.target_fps = target_fps
        self._last = perf_counter()

    def tick(self) -> float:
        now = perf_counter()
        dt = now - self._last
        target = 1 / self.target_fps
        if dt < target:
            sleep(target - dt)
            now = perf_counter()
            dt = now - self._last
        self._last = now
        return dt
