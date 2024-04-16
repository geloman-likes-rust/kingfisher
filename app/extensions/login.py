from flask import Blueprint
from app.shared.login import login_manager
from app.models.user import User

login = Blueprint("login", __name__)


@login.record_once
def on_load(state):
    login_manager.init_app(state.app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
