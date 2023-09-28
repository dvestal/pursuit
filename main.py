# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,too-few-public-methods,invalid-name
import time

from asciimatics.screen import ManagedScreen
import esper

from components import Intelligence, Position, Velocity
import systems
import tank


##########################
# Define a System
##########################
class IntelligenceSystem(esper.Processor):
    def process(self, *args, **kwargs):
        for _ent, (intel, pos, vel) in esper.get_components(Intelligence, Position, Velocity):
            intel.ai_engine.think(pos, vel)


##########################
# Game setup and main loop
##########################
def main():
    with ManagedScreen() as screen:
        max_board_size = min(screen.width, screen.height)

        # Instantiate a System (or more), and add them to the world
        ai_system = IntelligenceSystem()
        # esper.add_processor(ai_system, 9999)

        movement_system = systems.MovementSystem(max_board_size)
        # esper.add_processor(movement_system)

        renderable_system = systems.RenderSystem(screen, debug=True)
        # esper.add_processor(renderable_system, -1)

        # Create entities and assign Component instances to them
        _tank_one = tank.create(max_board_size)
        _tank_two = tank.create(max_board_size)
        _tank_three = tank.create(max_board_size)
        _tank_four = tank.create(max_board_size)

        # main loop
        running = True
        while running:
            try:
                while True:
                    screen.clear()

                    # esper.process()
                    ai_system.process()
                    movement_system.process()
                    renderable_system.process()

                    screen.refresh()
                    time.sleep(1)
            except KeyboardInterrupt:
                running = False


if __name__ == '__main__':
    # print("\nHeadless Example. Press Ctrl+C to quit!\n")
    main()
