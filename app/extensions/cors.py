from flask import Blueprint
from flask_cors import CORS
from app.shared.environments import allowed_origin

cors = Blueprint("cors", __name__)


@cors.record_once
def on_load(state):
    CORS(
        state.app,
        max_age=300,
        origins=allowed_origin or "http://localhost:5173",
        supports_credentials=True,
        expose_headers=["Authorization"],
    )
