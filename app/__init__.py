from flask import Flask
from app.extensions.cors import cors
from app.extensions.hasher import hasher

from app.routes.token import token
from app.routes.accounts import accounts
from app.routes.companies import companies
from app.routes.authentication import authentication

from app.queries.create_super_admin import create_super_admin

app = Flask(__name__)

# FLASK EXTENSIONS
app.register_blueprint(cors)
app.register_blueprint(hasher)

# API ROUTES
app.register_blueprint(token)
app.register_blueprint(accounts)
app.register_blueprint(companies)
app.register_blueprint(authentication)

with app.app_context():
    create_super_admin()
