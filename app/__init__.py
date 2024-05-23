from flask import Flask
from app.extensions.cors import cors
from app.extensions.hasher import hasher
from app.routes.accounts import accounts
from app.routes.authentication import authentication
from app.queries.accounts import create_super_admin

app = Flask(__name__)
app.config.from_prefixed_env()

app.register_blueprint(cors)
app.register_blueprint(hasher)
app.register_blueprint(accounts)
app.register_blueprint(authentication)

with app.app_context():
    create_super_admin()
