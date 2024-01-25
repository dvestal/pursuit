# pylint: disable=global-statement, line-too-long, invalid-name, missing-function-docstring, missing-module-docstring

import json
import random
import sys

import socketio


logger = True
engineio_logger = False

sio = socketio.Client(logger=logger, engineio_logger=engineio_logger)

my_sid = None
my_tank = None

###############################################################################
# Authentication Methods
###############################################################################

def send_authentication():
    username = sys.argv[1]
    password = sys.argv[2]
    sio.emit('authenticate', {'data': f'{username}:{password}'})


@sio.event
def connect():
    print('connected to server')
    send_authentication()


@sio.event
def auth_response(message):
    global my_sid
    global my_tank

    print(f'auth_response: {message}')
    if message['data'] == 'SUCCESSFUL':
        my_sid = message['sid']
        my_tank = message['tank']
        sio.emit('game_queue', {'data': 'queue'})

###############################################################################
# Game Update Handler
###############################################################################

@sio.event
def game_start(message):
    global my_tank
    print(f'game_start: {message}')
    my_tank = message['data']

@sio.event
def game_update(message):
    # Convert the message string to an object that you can use
    game_update_message = json.loads(message['data'])

    # So that it is easier to see your actions, this will only show your tank. Comment this out to see all tanks.
    tank = next((t for t in game_update_message['tanks'] if t['name'] == my_tank), None)
    if tank:
        print(f'game_update: {tank}')

    # Uncomment the following line to see all tanks and game world information.
    # print(f'game_update: {message}')

    # This is where you will add your code to control your tank.

    # Tank actions you can emit
    #   tank_action_change_direction
    #   tank_action_change_speed
    #   tank_action_shoot

    # Example code to move your tank randomly.
    action = random.choices(
        population=['MOVE', 'SHOOT', 'NONE'],
        weights=[0.8, 0.15, 0.05],
    )
    if action[0] == 'MOVE':
        print('action: move')
        move()
    elif action[0] == 'SHOOT':
        print('action: shoot')
        sio.emit('tank_action_shoot')
    else:   # action == 'NONE'
        print('action: none')

###############################################################################
# Action Methods
###############################################################################

def move():
    move_or_speed = random.choice(['MOVE', 'SPEED'])
    if move_or_speed == 'MOVE':
        direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        print(f'change_direction: {direction}')
        sio.emit('tank_action_change_direction', {'data': direction})
    else:   # move_or_speed == 'SPEED'
        velocity = random.randint(0, 2)
        print(f'tank_action_change_speed: {velocity}')
        sio.emit('tank_action_change_speed', {'data': velocity})


###############################################################################
# Start the Application
###############################################################################

if __name__ == '__main__':
    sio.connect('http://localhost:5000')
    sio.wait()
