from flask import Flask
#from models.UserManager import UserManager
from flask_login import UserMixin, LoginManager
from src.AuthenticationManager import *
from src.client import bootstrap_system



def valid_time(time):
    return time > 0

app = Flask(__name__)

app.secret_key = "This is a very secret key"


# Authentication manager and System setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

auth_manager = AuthenticationManager(login_manager)
system = bootstrap_system(auth_manager)

@login_manager.user_loader
def load_user(user_id):
    return system.get_user_by_id(user_id)

   