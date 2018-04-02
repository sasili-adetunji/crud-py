from api import db, ma, app
from api.helpers import hash_pwd
import datetime
import jwt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    def __init__(self, email, password):
        self.email = email
        self.password = hash_pwd(password)

    def encode_auth_token(self, _id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=50000),
                'iat': datetime.datetime.utcnow(),
                'sub': _id
            }
            return jwt.encode(
                    payload, 
                    app.config.get('SECRET_KEY'), 
                    algorithm='HS256',
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('email', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)