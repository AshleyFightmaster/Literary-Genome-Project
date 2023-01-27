from flask import Flask
from config import Config
from flask_migrate import Migrate
from .models import db, User
from .auth.routes import auth
from flask_login import LoginManager
from .books.routes import books

app = Flask(__name__)

app.config.from_object(Config)

login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# register Blueprints
app.register_blueprint(auth)
app.register_blueprint(books)

# initialize our database to work with our app
db.init_app(app)
migrate = Migrate(app, db)
login_manager.init_app(app)

from . import routes
from . import models