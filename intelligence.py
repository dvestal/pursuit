# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,too-few-public-methods,invalid-name
from random import randint, randrange

from components import Position, Velocity
import entities.bullet

class Wander:
    def think(self, pos: Position, vel: Velocity):
        vel.x = randint(-1, 1)
        vel.y = randint(-1, 1)

        fire_bullet = randrange(0, 100)
        if fire_bullet <= 25:
            entities.bullet.create('UP', pos.x, pos.y)
