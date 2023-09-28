# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,too-few-public-methods,invalid-name
from asciimatics.screen import Screen
import esper

from components import Intelligence, Position, Projectile, Renderable

class RenderSystem(esper.Processor):
    def __init__(self, screen: Screen, debug=False):
        super().__init__()
        self.debug = debug
        self.screen = screen

    def process(self, *args, **kwargs):
        self.show_background()
        if self.debug:
            self.show_screen_info()
        self.show_tanks()
        self.show_bullets()

    def show_background(self):
        max_size = min(self.screen.width, self.screen.height)
        self.screen.move(0, 0)
        self.screen.fill_polygon([[(0, 0), (max_size, 0), (max_size, max_size), (0, max_size)]])

    def show_screen_info(self):
        width = self.screen.width
        height = self.screen.height

        max_size = min(width, height)
        labels_x = max_size + 5

        self.screen.print_at(f"Screen[{width}, {height}]",
                                 labels_x, 0,
                                 colour=Screen.COLOUR_WHITE,
                                 attr=Screen.A_BOLD,
                                 bg=Screen.COLOUR_YELLOW)

    def show_tanks(self):
        index = 1
        for ent, (_rend, pos, ai) in esper.get_components(Renderable, Position, Intelligence):
            if self.debug:
                msg = f"Entity[{ent}] Location[{pos.x}, {pos.y}] AI [{ai.ai_engine.__class__.__name__}]"
                self.screen.print_at(msg,
                                    min(self.screen.width, self.screen.height) + 5, index,
                                    colour=Screen.COLOUR_DEFAULT,
                                    attr=Screen.A_BOLD,
                                    bg=Screen.COLOUR_YELLOW)

            # Move to the position of the tank and draw it
            self.screen.print_at(f'T[{ent}]', pos.x, pos.y,
                                 bg=Screen.COLOUR_WHITE)

            # Increment the index of the object so that the debug output can be placed correctly
            index += 1

    def show_bullets(self):
        # Draw the bullets
        for ent, (_proj_id, pos) in esper.get_components(Projectile, Position):
            # Move to the position of the tank and draw it
            self.screen.print_at(f"B[{ent}]", pos.x, pos.y, bg=Screen.COLOUR_WHITE)
