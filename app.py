from flask import Flask
from src.utils.db import db
from src.utils.api import api
from src.routes.category import ns_category
from src.routes.products import ns_product
import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database', 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = secrets.token_hex(16)

db.init_app(app)
api.init_app(app)
api.add_namespace(ns_category)
api.add_namespace(ns_product)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)