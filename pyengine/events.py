"""Typed event dispatch with deterministic listener ordering."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable, DefaultDict


@dataclass(frozen=True, slots=True)
class Event:
    """Engine event payload."""

    name: str
    data: dict[str, Any] = field(default_factory=dict)


Listener = Callable[[Event], None]


class EventBus:
    """Synchronous publish/subscribe event bus."""

    def __init__(self) -> None:
        self._listeners: DefaultDict[str, list[Listener]] = defaultdict(list)

    def subscribe(self, name: str, listener: Listener) -> None:
        if listener not in self._listeners[name]:
            self._listeners[name].append(listener)

    def unsubscribe(self, name: str, listener: Listener) -> None:
        if listener in self._listeners[name]:
            self._listeners[name].remove(listener)

    def emit(self, event: Event | str, **data: Any) -> None:
        payload = event if isinstance(event, Event) else Event(event, data)
        for listener in tuple(self._listeners.get(payload.name, ())):
            listener(payload)
