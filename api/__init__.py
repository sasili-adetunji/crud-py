import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)

app_settings = os.getenv(
    'APP_SETTINGS',
    'api.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

db = SQLAlchemy(app)
ma = Marshmallow(app)
