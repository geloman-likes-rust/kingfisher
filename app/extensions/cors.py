from os import getenv
from flask import Blueprint
from flask_cors import CORS

cors = Blueprint("cors", __name__)


@cors.record_once
def on_load(state):
    CORS(state.app, origins=getenv("ALLOWED_ORIGIN") or "http://localhost:5173")
