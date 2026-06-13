"""Input state that can be fed by any platform adapter."""

from __future__ import annotations


class InputState:
    """Tracks pressed, just-pressed, and just-released actions."""

    def __init__(self) -> None:
        self._pressed: set[str] = set()
        self._just_pressed: set[str] = set()
        self._just_released: set[str] = set()

    def press(self, action: str) -> None:
        if action not in self._pressed:
            self._just_pressed.add(action)
        self._pressed.add(action)

    def release(self, action: str) -> None:
        if action in self._pressed:
            self._just_released.add(action)
        self._pressed.discard(action)

    def pressed(self, action: str) -> bool:
        return action in self._pressed

    def just_pressed(self, action: str) -> bool:
        return action in self._just_pressed

    def just_released(self, action: str) -> bool:
        return action in self._just_released

    def end_frame(self) -> None:
        self._just_pressed.clear()
        self._just_released.clear()
