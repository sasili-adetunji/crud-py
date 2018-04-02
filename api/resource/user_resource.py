from flask_restful import Resource
from flask import Blueprint, request, make_response, jsonify
from api.helpers import validate_request
from api import db, app, bcrypt

from api.models.user import user_schema, users_schema, User


class RegisterResource(Resource):

    @validate_request((str, 'email', 'password'))
    def post(self):
        # get the post data
        post_data = request.get_json()
        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        if user:
            return  {
                'status': 'fail',
                'message': 'This account already exists and active'
            }
        else:
            try:
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password'),
                )

                # insert the user
                db.session.add(user)
                db.session.commit()
                return {
                    'status': 'success',
                    'message': 'Successfully registered. Login with your email',
                }
            except Exception as e:
                print(e)
                return {
                    'status': 'fail',
                    'message': 'Try again'
                }
class LoginResource(Resource):

    @validate_request((str, 'email', 'password'))
    def post(self):
        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            user = User.query.filter_by(
                email=post_data.get('email')
            ).first()
            if user:
                if bcrypt.check_password_hash(user.password, post_data.get('password')):
                    auth_token = user.encode_auth_token(user.id)
                    if auth_token:
                        return {
                            'status': 'success',
                            'message': 'Successfully logged in.',
                            'auth_token': auth_token.decode()
                        }
                else:
                    return {
                        'status': 'fail',
                        'message': 'Login credentials is incorrect.'
                    }
        except Exception as e:
            return {
                'status': 'fail',
                'message': 'Try again'
            }
class UserDetailResource(Resource):

    def get(self, id):
        user = User.query.get(id)
        return user_schema.jsonify(user)

    def put(self, id):
        user = User.query.get(id)
        username = request.json['username']
        email = request.json['email']

        user.email = email
        user.username = username

        db.session.commit()
        return user_schema.jsonify(user)

    def delete(self, id):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()

        return user_schema.jsonify(user)
