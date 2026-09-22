"""Latency-tolerant action prediction and authoritative reconciliation.

The client is allowed to apply an action immediately.  Server snapshots are
then reconciled by moving the client toward the authoritative position rather
than sleeping before every action.  The module is deliberately transport
agnostic so it can be embedded in a game client or tested offline.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import hypot
from typing import Iterable


@dataclass(frozen=True)
class Vec2:
    x: float
    y: float

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vec2":
        return Vec2(self.x * scalar, self.y * scalar)

    def distance_to(self, other: "Vec2") -> float:
        return hypot(self.x - other.x, self.y - other.y)


@dataclass(frozen=True)
class Action:
    sequence: int
    delta: Vec2


@dataclass(frozen=True)
class Snapshot:
    acknowledged_sequence: int
    position: Vec2


class RubberbandController:
    """Predict actions immediately and reconcile with server snapshots.

    ``correction_speed`` is expressed as a fraction of remaining error per
    second.  A value of 0.0 disables smoothing; ``max_correction_speed``
    prevents large corrections from creating a visible teleport.  Actions are
    never delayed based on round-trip time.
    """

    def __init__(
        self,
        position: Vec2 = Vec2(0.0, 0.0),
        *,
        correction_speed: float = 12.0,
        max_correction_speed: float = 100.0,
        snap_distance: float = 0.0,
    ) -> None:
        if correction_speed < 0 or max_correction_speed <= 0 or snap_distance < 0:
            raise ValueError("correction speeds must be positive and snap distance non-negative")
        self.position = position
        self._next_sequence = 1
        self._pending: list[Action] = []
        self._target: Vec2 | None = None
        self._correction_speed = correction_speed
        self._max_correction_speed = max_correction_speed
        self._snap_distance = snap_distance

    @property
    def pending_actions(self) -> tuple[Action, ...]:
        return tuple(self._pending)

    def apply_action(self, delta: Vec2) -> Action:
        """Apply and queue an action immediately; no ping-dependent sleep."""
        action = Action(self._next_sequence, delta)
        self._next_sequence += 1
        self.position = self.position + delta
        self._pending.append(action)
        return action

    def apply_actions(self, deltas: Iterable[Vec2]) -> tuple[Action, ...]:
        return tuple(self.apply_action(delta) for delta in deltas)

    def reconcile(self, snapshot: Snapshot) -> None:
        """Drop acknowledged input and smoothly target the server position."""
        self._pending = [a for a in self._pending if a.sequence > snapshot.acknowledged_sequence]
        # Re-apply unacknowledged actions to the authoritative base. This makes
        # reconciliation deterministic even when several packets are delayed.
        predicted = snapshot.position
        for action in self._pending:
            predicted = predicted + action.delta
        self._target = predicted
        if self._correction_speed == 0:
            self.position = predicted
            self._target = None
            return
        if self.position.distance_to(predicted) >= self._snap_distance > 0:
            self.position = predicted
            self._target = None

    def tick(self, delta_seconds: float) -> Vec2:
        if delta_seconds < 0:
            raise ValueError("delta_seconds cannot be negative")
        if self._target is None or self.position == self._target:
            return self.position
        error = self._target - self.position
        distance = hypot(error.x, error.y)
        if self._correction_speed == 0:
            self.position = self._target
            self._target = None
            return self.position
        travel = min(distance, self._max_correction_speed * delta_seconds,
                     distance * self._correction_speed * delta_seconds)
        self.position = self.position + error * (travel / distance) if distance else self._target
        if self.position == self._target:
            self._target = None
        return self.position
