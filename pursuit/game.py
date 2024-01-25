from enum import Enum
import json
import math


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Tank:
    def __init__(self, name, x, y, direction: Direction = Direction.UP):
        self.name = name
        self.x = x
        self.y = y
        self.direction = direction
        self.velocity = 0


class Bullet:
    def __init__(self, x, y, direction: Direction = Direction.UP):
        self.x = x
        self.y = y
        self.direction = direction
        self.velocity = 2


class GameWorld:
    def __init__(self, sio, width, height):
        self.sio = sio
        self.width = width
        self.height = height
        self.tanks = []
        self.bullets = []
        self.tombstone_bullet = []
        self.tombstone_tank = []

    def add_tank(self, tank):
        self.tanks.append(tank)

    def remove_tanks(self, tank):
        for tank in self.tombstone_tank:
            if tank in self.tanks:
                self.tanks.remove(tank)
        self.tombstone_tank = []

    def add_bullet(self, bullet):
        self.bullets.append(bullet)

    def remove_bullets(self):
        for bullet in self.tombstone_bullet:
            if bullet in self.bullets:
                self.bullets.remove(bullet)
        self.tombstone_bullet = []

    def update(self):
        self.update_bullets()
        self.remove_bullets()

        self.update_tanks()
        self.detect_collisions()

    def update_tanks(self):
        for tank in self.tanks:
            if tank.velocity > 0:
                if tank.direction == Direction.UP:
                    tank.y -= tank.velocity
                elif tank.direction == Direction.DOWN:
                    tank.y += tank.velocity
                elif tank.direction == Direction.LEFT:
                    tank.x -= tank.velocity
                elif tank.direction == Direction.RIGHT:
                    tank.x += tank.velocity

                if tank.x < 0:
                    tank.x = 0
                elif tank.x > self.width:
                    tank.x = self.width

                if tank.y < 0:
                    tank.y = 0
                elif tank.y > self.height:
                    tank.y = self.height

    def update_bullets(self):
        for bullet in self.bullets:
            if bullet.direction == Direction.UP:
                bullet.y -= bullet.velocity
            elif bullet.direction == Direction.DOWN:
                bullet.y += bullet.velocity
            elif bullet.direction == Direction.LEFT:
                bullet.x -= bullet.velocity
            elif bullet.direction == Direction.RIGHT:
                bullet.x += bullet.velocity

            if bullet.x < 0 or bullet.x > self.width or bullet.y < 0 or bullet.y > self.height:
                self.tombstone_bullet.append(bullet)

    def detect_collisions(self):
        for bullet in self.bullets:
            for tank in self.tanks:
                distance = math.hypot(bullet.x - tank.x, bullet.y - tank.y)
                if distance <= 1:
                    self.tombstone_bullet.append(bullet)
                    self.tombstone_tank.append(tank)
                    self.sio.emit('remove_tank', {'data': tank.name})

    def check_end_game(self) -> bool:
        game_over = False

        if len(self.tanks) <= 2:
            print(f'Game Over! Winner: {self.tanks[0].name}')
            game_over = True

        return game_over

    def to_json(self):
        data = {
            "width": self.width,
            "height": self.height,
            "tanks": [],
            "bullets": []
        }

        for tank in self.tanks:
            tank_data = {
                "name": tank.name,
                "x": tank.x,
                "y": tank.y,
                "direction": tank.direction.name,
                "velocity": tank.velocity
            }
            data["tanks"].append(tank_data)

        for bullet in self.bullets:
            bullet_data = {
                "x": bullet.x,
                "y": bullet.y,
                "direction": bullet.direction.name,
                "velocity": bullet.velocity
            }
            data["bullets"].append(bullet_data)

        return json.dumps(data)
