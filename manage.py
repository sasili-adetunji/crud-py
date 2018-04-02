from flask import Flask, request, jsonify
from api import db, app
from api.models.user import user_schema, users_schema, User
from flask_restful import Api
from api.resource.user_resource import UserResource, UserDetailResource


api = Api(app)

api.add_resource(
    UserResource,
    '/api/v1/users',
    '/api/v1/users/',
    endpoint='users')

api.add_resource(
    UserDetailResource,
    '/api/v1/users/<string:id>',
    '/api/v1/users/<string:id>/',
    endpoint='user_details')


if __name__ == "__main__":
    app.run()

