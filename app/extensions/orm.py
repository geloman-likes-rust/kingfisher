from flask import Blueprint
from app.shared.orm import db

orm = Blueprint("orm", __name__)


@orm.record_once
def on_load(state):
    db.init_app(state.app)
