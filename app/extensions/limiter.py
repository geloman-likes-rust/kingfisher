from flask import Blueprint
from app.shared.limiter import limiter as rate_limiter


limiter = Blueprint("limiter", __name__)


@limiter.record_once
def on_load(state):
    rate_limiter.init_app(state.app)
