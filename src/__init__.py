from flask import Flask
from flask_migrate import Migrate
from .database import db
from .models import *

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@db/app"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.main import main
    app.register_blueprint(main)

    from .routes.chambres import chambres
    app.register_blueprint(chambres)

    from .routes.reservations import reservations
    app.register_blueprint(reservations)

    return app