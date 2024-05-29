from flask import Blueprint
from app.shared.hasher import bcrypt

hasher = Blueprint("hasher", __name__)


@hasher.record_once
def on_load(state):
    bcrypt.init_app(state.app)
