# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,too-few-public-methods,invalid-name
import esper

from components import Position, Projectile, Velocity


class MovementSystem(esper.Processor):
    def __init__(self, max_board_size):
        self.max_board_size = max_board_size - 1

    def process(self, *args, **kwargs):
        for ent, (pos, vel) in esper.get_components(Position, Velocity):
            new_x = pos.x + int(vel.x)
            new_y = pos.y + int(vel.y)

            # If this object is a projectile we want to allow it to continue when it hits a wall
            if esper.has_component(ent, Projectile):
                pos.x = new_x
                pos.y = new_y

            # If the object is not a projectile, keep it within the walls
            else:
                # Guards to make sure we do not go off the map
                if 0 <= new_x <= self.max_board_size:
                    pos.x = new_x

                if 0 <= new_y <= self.max_board_size:
                    pos.y = new_y

            if 0 > new_x > self.max_board_size or 0 > new_y > self.max_board_size:
                esper.delete_entity(ent)
