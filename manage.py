from flask import Flask, request, jsonify
from api import db, app
from api.models.user import user_schema, users_schema, User
from flask_restful import Api
from api.resource.user_resource import UserDetailResource, LoginResource, RegisterResource


api = Api(app)


api.add_resource(
    RegisterResource,
    '/api/v1/register/',
    '/api/v1/register',
    endpoint='register'
)

api.add_resource(
    LoginResource,
    '/api/v1/login/',
    '/api/v1/login',
    endpoint='login'
)

api.add_resource(
    UserDetailResource,
    '/api/v1/users/<string:id>',
    '/api/v1/users/<string:id>/',
    endpoint='user_details')


if __name__ == "__main__":
    app.run()

