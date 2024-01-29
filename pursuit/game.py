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
    direction: Direction = Direction.UP

@component
class Bullet:
    direction: Direction

@component
class Position:
    x: int = 0
    y: int = 0

@component
class Velocity:
    x: int = 0
    y: int = 0

class GameWorld:
    def __init__(self, sio, width, height):
        self.sio = sio
        self.width = width
        self.height = height

        esper.add_processor(MovementSystem(self.width, self.height), 999)
        # esper.add_processor(BulletMovementSystem(self.width, self.height), 999)

    def spawn_tank(self):
        tank = esper.create_entity()

        tank_name = f"{uuid.uuid4()}"
        x = random.randint(0, 99)
        y = random.randint(0, 99)
        esper.add_component(tank, Tank(tank_name))
        esper.add_component(tank, Position(x, y))
        esper.add_component(tank, Velocity(0, 0))
        return tank_name

    def find_tank(self, name) -> (int, Tank):
        for ent, (tank) in esper.get_component(Tank):
            if tank.name == name:
                return ent, tank
        return None, None

    def set_tank_direction(self, name, direction):
        (ent, tank) = self.find_tank(name)
        if tank:
            tank.direction = direction

            vel = esper.component_for_entity(ent, Velocity)
            new_vel = convert_velocity_direction(vel, tank.direction, direction)
            vel.x = new_vel.x
            vel.y = new_vel.y


    def set_tank_velocity(self, name, speed):
        (ent, tank) = self.find_tank(name)
        if tank:
            vel = esper.component_for_entity(ent, Velocity)
            if tank.direction == Direction.UP:
                vel.y = speed
            if tank.direction == Direction.DOWN:
                vel.y = speed * -1
            if tank.direction == Direction.LEFT:
                vel.x = speed * -1
            if tank.direction == Direction.RIGHT:
                vel.x = speed


    def spawn_bullet(self, name):
        (ent, tank) = self.find_tank(name)
        if tank:
            bullet = esper.create_entity()
            tank_pos = esper.component_for_entity(ent, Position)
            esper.add_component(bullet, Bullet(direction=tank.direction))
            esper.add_component(bullet, Position(tank_pos.x, tank_pos.y))
            if tank.direction == Direction.UP:
                esper.add_component(bullet, Velocity(0, 2))
            if tank.direction == Direction.DOWN:
                esper.add_component(bullet, Velocity(0, -2))
            if tank.direction == Direction.LEFT:
                esper.add_component(bullet, Velocity(-2, 0))
            if tank.direction == Direction.RIGHT:
                esper.add_component(bullet, Velocity(2, 0))


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
                "direction": tank.direction.name,
                "velocity": speed_from_velocity_and_direction(vel, tank.direction)
            }
            data["tanks"].append(tank_data)

        for ent, (bullet, pos, vel) in esper.get_components(Bullet, Position, Velocity):
            bullet_data = {
                "x": pos.x,
                "y": pos.y,
                "direction": bullet.direction.name,
                "velocity": speed_from_velocity_and_direction(vel, bullet.direction)
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
            pos.x += vel.x
            pos.y += vel.y


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
