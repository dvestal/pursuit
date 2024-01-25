# pylint: disable=global-statement, line-too-long, missing-function-docstring, missing-module-docstring

import uuid

from flask import Blueprint
from werkzeug.security import check_password_hash

from . import app, db, sio
from .game import GameWorld, Bullet, Tank, Direction
from .models import User


game = Blueprint('game', __name__)

game_world = None


###############################################################################
# Game Update Background Task
###############################################################################

def background_thread():
    global game_world

    while True:
        if game_world is None:
            game_world = GameWorld(sio, 100, 100)

            # TODO: Choose the players or assign bots to the tanks

            # Create 4 tanks and add them to the game world
            with app.app_context():
                stmt = db.select(User).where(User.username.is_("testy1"))
                user = db.session.scalars(stmt).one_or_none()
                if user:
                    tank_id = f'{uuid.uuid4()}'
                    tank1 = Tank(f"{uuid.uuid4()}", 10, 10, Direction.RIGHT)
                    game_world.add_tank(tank1)
                    user.tank = tank_id
                    # db.session.commit()
                    sio.emit('game_start', {'data': tank_id}, room=user.sid)


            with app.app_context():
                stmt = db.select(User).where(User.username.is_("testy2"))
                user = db.session.scalars(stmt).one_or_none()
                if user:
                    tank_id = f'{uuid.uuid4()}'
                    tank2 = Tank(f"{uuid.uuid4()}", 10, 90, Direction.DOWN)
                    game_world.add_tank(tank2)
                    user.tank = tank_id
                    # db.session.commit()
                    sio.emit('game_start', {'data': tank_id}, room=user.sid)

            with app.app_context():
                stmt = db.select(User).where(User.username.is_("testy3"))
                user = db.session.scalars(stmt).one_or_none()
                if user:
                    tank_id = f'{uuid.uuid4()}'
                    tank3 = Tank(tank_id, 90, 90, Direction.LEFT)
                    game_world.add_tank(tank3)
                    user.tank = tank_id
                    db.session.commit()
                    sio.emit('game_start', {'data': tank_id}, room=user.sid)

            with app.app_context():
                stmt = db.select(User).where(User.username.is_("testy4"))
                user = db.session.scalars(stmt).one_or_none()
                if user:
                    tank_id = f'{uuid.uuid4()}'
                    tank4 = Tank(tank_id, 90, 10, Direction.UP)
                    game_world.add_tank(tank4)
                    user.tank = tank_id
                    db.session.commit()
                    sio.emit('game_start', {'data': tank_id}, room=user.sid)


        sio.sleep(1)
        game_world.update()

        if game_world.check_end_game():
            game_world = None
            sio.emit('game_end', {'data': 'game over'})
            continue


        game_world_update_message = game_world.to_json()
        sio.emit('game_update', {'data': f'{game_world_update_message}'})


###############################################################################
# Handlers
###############################################################################

@sio.event
def authenticate(sid, message):
    with app.app_context():
        print(f'Authenticate sid={sid} message={message}')

        bearer = message['data'].split(':')
        stmt = db.select(User).where(User.username.is_(bearer[0]))
        user = db.session.scalars(stmt).one_or_none()

        print(f'Authentication: User={user}')
        data_object = {'data': "UNSUCCESSFUL", 'sid': sid}
        if user and check_password_hash(user.password, bearer[1]):
            # update record to mark user online and their sid
            user.online = True
            user.sid = sid
            db.session.commit()
            data_object['data'] = "SUCCESSFUL"
            data_object['tank'] = user.tank

        sio.emit('auth_response', data_object, room=sid)


@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)


@sio.event
def connect(sid, environ):
    print(f'Client connected: {environ}')
    sio.emit('auth_request', {'data': f'{sid}'}, room=sid)


@sio.event
def disconnect(sid):
    with app.app_context():
        stmt = db.select(User).where(User.sid.is_(sid))
        user = db.session.scalars(stmt).one_or_none()
        if user:
            user.online = False
            user.sid = None
            db.session.commit()
        print(f'Client disconnected [{user.username}, {sid}]')


@sio.event
def remove_tank(tank):
    with app.app_context():
        stmt = db.select(User).where(User.tank.is_(tank))
        user = db.session.scalars(stmt).one_or_none()
        if user:
            user.tank = None
            db.session.commit()
        print(f'Remove Tank [{user.username}, {tank}]')
        sio.emit('remove_tank', {'data': tank})

###############################################################################
# Tank Actions
###############################################################################

@sio.event
def tank_action_change_direction(sid, message):
    with app.app_context():
        stmt = db.select(User).where(User.sid.is_(sid))
        user = db.session.scalars(stmt).one_or_none()
        if user:
            tank = next((t for t in game_world.tanks if t.name == user.tank), None)
            if tank:
                direction = Direction[message['data']]
                print(f'tank_action_change_direction: [{user.username} {tank.name} {tank.direction} {direction}]')
                tank.direction = direction


@sio.event
def tank_action_change_speed(sid, message):
    with app.app_context():
        stmt = db.select(User).where(User.sid.is_(sid))
        user = db.session.scalars(stmt).one_or_none()
        if user:
            tank = next((t for t in game_world.tanks if t.name == user.tank), None)
            if tank:
                velocity = int(message['data'])
                print(f'tank_action_change_speed: [{user.username} {tank.name} {tank.velocity} {velocity}]')
                tank.velocity = velocity


@sio.event
def tank_action_shoot(sid):
    with app.app_context():
        stmt = db.select(User).where(User.sid.is_(sid))
        user = db.session.scalars(stmt).one_or_none()
        if user:
            tank = next((t for t in game_world.tanks if t.name == user.tank), None)
            if tank:
                print(f'tank_action_shoot: [{user.username} {tank.name} {tank.x} {tank.y} {tank.direction}]')
                bullet = Bullet(tank.x, tank.y, tank.direction)
                game_world.add_bullet(bullet)

# @sio.event
# def my_event(sid, message):
#     sio.emit('my_response', {'data': message['data']}, room=sid)


# @sio.event
# def my_broadcast_event(sid, message):
#     sio.emit('my_response', {'data': message['data']})


# @sio.event
# def join(sid, message):
#     sio.enter_room(sid, message['room'])
#     sio.emit('my_response', {'data': 'Entered room: ' + message['room']},
#              room=sid)


# @sio.event
# def leave(sid, message):
#     sio.leave_room(sid, message['room'])
#     sio.emit('my_response', {'data': 'Left room: ' + message['room']},
#              room=sid)


# @sio.event
# def close_room(sid, message):
#     sio.emit('my_response',
#              {'data': 'Room ' + message['room'] + ' is closing.'},
#              room=message['room'])
#     sio.close_room(message['room'])


# @sio.event
# def my_room_event(sid, message):
#     sio.emit('my_response', {'data': message['data']}, room=message['room'])
