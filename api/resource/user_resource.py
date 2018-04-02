from flask_restful import Resource
from flask import Flask, request, jsonify
from api import db, app

from api.models.user import user_schema, users_schema, User


class UserResource(Resource):

    def post(self):
        username = request.json['username']
        email = request.json['email']
        
        new_user = User(username, email)
        db.session.add(new_user)
        db.session.commit()
        res = {'email': new_user.email, 'username': new_user.username, 'id': new_user.id}
        return jsonify(res)

    def get(self):
        all_users = User.query.all()
        result = users_schema.dump(all_users)
        return jsonify(result.data)


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
