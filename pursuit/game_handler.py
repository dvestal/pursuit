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

def wait_for_bot_connections():
    while True: # Bot Connection Check Loop
        print("Bot Connection Check Loop")
        with app.app_context():
            # Check for connected bots. If the four are not yet connected then just wait.
            query = db.session.query(User).filter(User.bot.is_(True), User.online.is_(True))
            bot_count = db.session.scalars(query).all()

            print(f"Found {len(bot_count)} bots online")
            if len(bot_count) == 4:
                print("  Found enough bots online to start. Starting to check for users.")
                stmt = db.select(User).where(User.bot.is_(False), User.online.is_(True))
                online_users = db.session.scalars(stmt).all()
                print(f"Found {len(online_users)} users online")
                return # Break out of the Bot Connection Check Loop

        sio.sleep(5)


def next_online_user():
    with app.app_context():
        stmt = db.select(User).where(User.bot.is_(False), User.online.is_(True))
        online_users = db.session.scalars(stmt).all()
        for user in online_users:
            yield user


def next_online_bot():
    with app.app_context():
        stmt = db.select(User).where(User.bot.is_(True), User.online.is_(True))
        online_users = db.session.scalars(stmt).all()
        for bot in online_users:
            yield bot


def next_online_player():
    for user in next_online_user():
        yield user

    for bot in next_online_bot():
        yield bot


def background_thread():
    global game_world

    while True:
        if game_world is None:
            # wait_for_bot_connections()
            game_world = GameWorld(sio, 100, 100)

            # # TODO: Choose the players or assign bots to the tanks
            # tanks = []
            # tanks.append(Tank(f"{uuid.uuid4()}", 10, 10, Direction.RIGHT))
            # tanks.append(Tank(f"{uuid.uuid4()}", 10, 90, Direction.DOWN))
            # tanks.append(Tank(f"{uuid.uuid4()}", 90, 90, Direction.LEFT))
            # tanks.append(Tank(f"{uuid.uuid4()}", 90, 10, Direction.UP))

            # for (tank, player) in zip(tanks, next_online_player()):
            #     game_world.add_tank(tank)
            #     player.tank = tank.name
            #     sio.emit('game_start', {'data': tank.name}, room=player.sid)

        sio.sleep(1)
        game_world.update()

        # if game_world.check_end_game():
        #     game_world = None
        #     sio.emit('game_end', {'data': 'game over'})
        #     continue

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

            print(f"authenticate: tank [{user.tank}]")

            if not user.tank or not game_world.find_tank(user.tank):
                tank_name = game_world.spawn_tank()
                user.tank = tank_name
            db.session.commit()

            data_object['tank'] = user.tank
            data_object['data'] = "SUCCESSFUL"


        sio.emit('auth_response', data_object, room=sid)


@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)


@sio.event
def connect(sid, _environ):
    print(f'Client connected: {sid}')
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
            direction = Direction[message['data']]
            print(f'tank_action_change_direction: [{user.username} {user.tank} {direction}]')
            game_world.set_tank_direction(user.tank, direction)


@sio.event
def tank_action_change_speed(sid, message):
    with app.app_context():
        stmt = db.select(User).where(User.sid.is_(sid))
        user = db.session.scalars(stmt).one_or_none()
        if user:
            velocity = int(message['data'])
            print(f'tank_action_change_speed: [{user.username} {user.tank} {velocity}]')
            game_world.set_tank_velocity(user.tank, velocity)


@sio.event
def tank_action_shoot(sid):
    with app.app_context():
        stmt = db.select(User).where(User.sid.is_(sid))
        user = db.session.scalars(stmt).one_or_none()
        if user:
            print(f'tank_action_shoot: [{user.username}]')
            game_world.spawn_bullet(user.tank)

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
