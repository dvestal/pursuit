# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,too-few-public-methods,invalid-name
"""
Game Component Objects
"""

from dataclasses import dataclass as component


@component
class Velocity:
    x: float = 0.0
    y: float = 0.0


@component
class Position:
    x: int = 0
    y: int = 0


@component
class Renderable:
    pass


class TankIntelligence:
    def think(self, pos: Position, vel: Velocity):
        pass


@component
class Intelligence:
    ai_engine: TankIntelligence


@component
class Projectile:
    pass
