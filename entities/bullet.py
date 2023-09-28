# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,too-few-public-methods,invalid-name
import esper

from components import Position, Projectile, Renderable, Velocity


def create(direction, pos_x, pos_y) -> int:
    bullet = esper.create_entity()

    vel_x = 0.0
    vel_y = 0.0

    if direction == 'UP':
        vel_y = 2.0
    elif direction == 'DOWN':
        vel_y = -2.0
    elif direction == 'LEFT':
        vel_x = -2.0
    elif direction == 'RIGHT':
        vel_y = 2.0

    esper.add_component(bullet, Velocity(x=vel_x, y=vel_y))
    esper.add_component(bullet, Position(x=pos_x, y=pos_y))
    esper.add_component(bullet, Renderable())
    esper.add_component(bullet, Projectile())

    return bullet
