from flask import Blueprint
from flask_cors import CORS
from app.shared.environments import allowed_origin

cors = Blueprint("cors", __name__)


@cors.record_once
def on_load(state):
    five_minutes = 300
    CORS(
        state.app,
        max_age=five_minutes,
        origins=allowed_origin or "http://localhost:5173",
        expose_headers=["Authorization"],
    )
