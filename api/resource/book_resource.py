from flask_restful import Resource
from flask import Blueprint, request, make_response, jsonify
from api.helpers import validate_request
from api import db, app, bcrypt
from api.models.user import User
from api.models.books import Books



class BookResource(Resource):

    @validate_request((str, "book_title", "book_description"))
    def post(self):
        
        # get the auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                return {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # get the post data
                post_data = request.get_json()  
                
                # check if Records already exists
                books = Books.query.filter_by(book_title=post_data.get('book_title')).first()
                if not books:
                    try:
                        books = Books(
                            book_title=post_data.get('book_title'),
                            book_description=post_data.get('book_description'),
                        )
                        # insert the book
                        db.session.add(books)
                        db.session.commit()
                        return {
                            'status': 'success',
                            'message': 'Books Successfully recorded.',
                        }
                    except Exception as e:
                        print(e)
                        return {
                            'status': 'fail',
                            'message': 'Some error occurred. Please try again.'
                        }
                else:
                    return {
                        'status': 'fail',
                        'message': 'Books already exists.',
                    }
            return {
                'status': 'fail',
                'message': resp
            }
        else:
            return {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }

    def get(self):
        # get the token
        auth_header = request.headers.get('Authorization')

        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                return {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
        else:
            auth_token = ''

        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                books = Books.query.all()
                result = [{ "book_title": i.book_title,
                "book_description": i.book_description, "created_on": str(i.created_on), "updated_on": str(i.updated_on) } for i in books]
                if not books:
                    return {
                        'status': 'fail',
                        'message': 'No Records added yet'
                    }
                else:
                    return  {
                        'status': 'success',
                        'data': {
                            'records': result,
                        }
                    }
            return {
                'status': 'fail',
                'message': resp
            }
        else:
            return {
                'status': 'fail',
                'message': 'Provide a valid token.'
            }
