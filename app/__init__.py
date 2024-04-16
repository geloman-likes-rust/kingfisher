from flask import Flask
from app.shared.orm import db
from app.extensions.orm import orm
from app.extensions.cors import cors
from app.extensions.login import login
from app.extensions.hasher import hasher
from app.routes.accounts import accounts
from app.routes.authentication import authentication

app = Flask(__name__)
app.config.from_prefixed_env()

app.register_blueprint(orm)
app.register_blueprint(cors)
app.register_blueprint(login)
app.register_blueprint(hasher)
app.register_blueprint(accounts)
app.register_blueprint(authentication)

with app.app_context():
    db.create_all()
