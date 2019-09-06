from myvyosapp import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from flask import Flask
from flask_bootstrap import Bootstrap
from flask_session import Session
from flask_login import LoginManager

import redis





app = Flask(__name__)


app.config.from_object(config)

if (app.config['REDIS_URI']):
    app.config['SESSION_REDIS'] = redis.from_url(app.config['REDIS_URI'])

sess = Session()
sess.init_app(app)

login = LoginManager()
login.init_app(app)

db = SQLAlchemy()
migrate = Migrate(app, db)

bootstrap = Bootstrap()
bootstrap.init_app(app)
db.app = app
db.init_app(app)

## routes
from myvyosapp.site.routes import site
from myvyosapp.apiendpoint.routes import apiendpoint
app.register_blueprint(site)
app.register_blueprint(apiendpoint)
