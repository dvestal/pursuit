# pylint: disable=line-too-long, missing-function-docstring, missing-module-docstring

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', username=current_user.username)

@main.route('/lobby')
def lobby():
    online_users = User.query.filter_by(online=True, bot=False).all()
    return render_template('lobby.html', users=online_users)
