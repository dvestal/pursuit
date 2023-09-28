# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,too-few-public-methods,invalid-name
from random import randint

import esper

from components import Intelligence, Position, Renderable, Velocity

from intelligence import Wander


def create(max_board_size, ai_engine=None) -> int:
    tank = esper.create_entity()
    esper.add_component(tank, Velocity(x=0.0, y=0.0))

    pos_x = randint(0, max_board_size)
    pos_y = randint(0, max_board_size)
    esper.add_component(tank, Position(x=pos_x, y=pos_y))
    esper.add_component(tank, Renderable())

    # If an ai_engine was passed in use that, otherwise, default to Wandering
    if not ai_engine:
        ai_engine = Wander()
    esper.add_component(tank, Intelligence(ai_engine))

    return tank
