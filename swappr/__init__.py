import os
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///swappr.db'
app.config['TANDA'] = {
    'consumer_key': os.environ['SWAPPR_TANDA_API_KEY'],
    'consumer_secret': os.environ['SWAPPR_TANDA_API_SECRET'],
}
app.config['SECRET_KEY'] = os.environ['SWAPPR_SECRET_KEY']

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user.login"
login_manager.login_message = "Log In Please"

from .models import *

from .user import user as user_bp
from .shift import shift as shift_bp
from .manage import manage as manage_bp

BLUEPRINTS = [user_bp, shift_bp, manage_bp]

for blueprint in BLUEPRINTS:
    app.register_blueprint(blueprint)

from . import views
