"""
Pursuit Application
"""

# pylint: disable=global-statement, import-outside-toplevel, line-too-long, missing-function-docstring

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import socketio


app = Flask(__name__)
db = SQLAlchemy()

async_mode = 'threading'
instrument = False
thread = None

sio = socketio.Server(
    async_mode=async_mode,
    cors_allowed_origins=None if not instrument else [
        'http://localhost:5000',
        'https://admin.socket.io', # edit the allowed origins if necessary
    ]
)

admin_login = {
    'username': 'admin',
    'password': 'python',
}


def create_app():
    global thread

    if instrument:
        sio.instrument(auth=admin_login)

    app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

    app.config['SECRET_KEY'] = 'secret!'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'

    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .game_handler import game as game_blueprint
    app.register_blueprint(game_blueprint)

    from .game_handler import background_thread as game_background_thread
    if thread is None:
        thread = sio.start_background_task(game_background_thread)

    return app
