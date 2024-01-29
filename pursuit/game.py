from dataclasses import dataclass as component
from enum import Enum
import json
import math
import random
import uuid

import esper

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

@component
class Tank:
    name: str = None

@component
class Bullet:
    pass

@component
class Position:
    x: int = 0
    y: int = 0

@component
class Velocity:
    speed: int = 0
    direction: Direction = Direction.UP

class GameWorld:
    def __init__(self, sio, width, height):
        self.sio = sio
        self.width = width
        self.height = height

        esper.add_processor(MovementSystem(self.width, self.height), 999)
        esper.add_processor(OffscreenBulletSystem(self.width, self.height))
        # esper.add_processor(BulletMovementSystem(self.width, self.height), 999)

    def spawn_tank(self):
        tank = esper.create_entity()

        tank_name = f"{uuid.uuid4()}"
        x = random.randint(0, 99)
        y = random.randint(0, 99)
        esper.add_component(tank, Tank(tank_name))
        esper.add_component(tank, Position(x, y))
        esper.add_component(tank, Velocity(0))
        return tank_name

    def find_tank(self, name) -> (int, Tank):
        for ent, (tank) in esper.get_component(Tank):
            if tank.name == name:
                return ent, tank
        return None, None

    def set_tank_direction(self, name, direction):
        (ent, tank) = self.find_tank(name)
        if tank:
            vel = esper.component_for_entity(ent, Velocity)
            vel.direction = direction


    def set_tank_velocity(self, name, speed):
        (ent, tank) = self.find_tank(name)
        if tank:
            vel = esper.component_for_entity(ent, Velocity)
            vel.speed = speed


    def spawn_bullet(self, name):
        (ent, tank) = self.find_tank(name)
        if tank:
            bullet = esper.create_entity()
            tank_pos = esper.component_for_entity(ent, Position)
            tank_vel = esper.component_for_entity(ent, Velocity)
            esper.add_component(bullet, Bullet())
            esper.add_component(bullet, Position(tank_pos.x, tank_pos.y))
            esper.add_component(bullet, Velocity(2, tank_vel.direction))



    def update(self):
        esper.process()

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

        for ent, (tank, pos, vel) in esper.get_components(Tank, Position, Velocity):
            tank_data = {
                "name": tank.name,
                "x": pos.x,
                "y": pos.y,
                "direction": vel.direction.name,
                "velocity": vel.speed
            }
            data["tanks"].append(tank_data)

        for ent, (bullet, pos, vel) in esper.get_components(Bullet, Position, Velocity):
            bullet_data = {
                "x": pos.x,
                "y": pos.y,
                "direction": vel.direction.name,
                "velocity": vel.speed
            }
            data["bullets"].append(bullet_data)

        return json.dumps(data)


class MovementSystem:

    max_width: int
    max_height: int

    def __init__(self, max_width, max_height):
        self.max_width = max_width
        self.max_height = max_height

    def process(self):
        for ent, (pos, vel) in esper.get_components(Position, Velocity):
            if vel.direction == Direction.UP:
                pos.y += vel.speed
            if vel.direction == Direction.DOWN:
                pos.y -= vel.speed
            if vel.direction == Direction.LEFT:
                pos.x -= vel.speed
            if vel.direction == Direction.RIGHT:
                pos.x += vel.speed

            if esper.has_component(ent, Tank):
                pos.x = max(0, min(pos.x, self.max_width))
                pos.y = max(0, min(pos.y, self.max_height))


class OffscreenBulletSystem:

    max_width: int
    max_height: int

    def __init__(self, max_width, max_height):
        self.max_width = max_width
        self.max_height = max_height

    def process(self):
        for ent, (bullet, pos) in esper.get_components(Bullet, Position):
            if pos.x < 0 or pos.x > self.max_width or pos.y < 0 or pos.y > self.max_height:
                esper.delete_entity(ent)

def speed_from_velocity_and_direction(velocity, direction):
    if direction == Direction.UP or direction == Direction.DOWN:
        return velocity.y

    if direction == Direction.LEFT or direction == Direction.RIGHT:
        return velocity.x


def convert_velocity_direction(velocity, curr_direction, new_direction):
    if curr_direction == Direction.UP:
        if new_direction == Direction.RIGHT:
            velocity.x = velocity.y
            velocity.y = 0

        if new_direction == Direction.DOWN:
            velocity.y = velocity.y * -1
            velocity.x = 0

        if new_direction == Direction.LEFT:
            velocity.x = velocity.y * -1
            velocity.y = 0

    if curr_direction == Direction.RIGHT:
        if new_direction == Direction.UP:
            velocity.y = velocity.x
            velocity.x = 0

        if new_direction == Direction.DOWN:
            velocity.y = velocity.x * -1
            velocity.x = 0

        if new_direction == Direction.LEFT:
            velocity.x = velocity.x * -1
            velocity.y = 0

    if curr_direction == Direction.DOWN:
        if new_direction == Direction.UP:
            velocity.y = velocity.y * -1
            velocity.x = 0

        if new_direction == Direction.RIGHT:
            velocity.x = abs(velocity.y)
            velocity.y = 0

        if new_direction == Direction.LEFT:
            velocity.x = velocity.y
            velocity.y = 0

    if curr_direction == Direction.LEFT:
        if new_direction == Direction.UP:
            velocity.y = abs(velocity.x)
            velocity.x = 0

        if new_direction == Direction.RIGHT:
            velocity.x = velocity.x * -1
            velocity.y = 0

        if new_direction == Direction.DOWN:
            velocity.y = velocity.x
            velocity.x = 0

    return velocity
