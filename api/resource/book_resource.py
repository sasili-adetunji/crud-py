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
                result = [{ "book_title": i.book_title, "id": i.id,
                "book_description": i.book_description, "created_on": str(i.created_on), "updated_on": str(i.updated_on) } for i in books]
                if not books:
                    return {
                        'status': 'fail',
                        'message': 'No books added yet'
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

class BookDetailsResource(Resource):
    """
    Edits, Delete and Get Individual book details

    """

    def get(self, id):
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
                books = Books.query.filter_by(id=id).first()
                if not books:
                    return {
                        'status': 'fail',
                        'message': 'No books with this ID'
                    }
                else:
                    return {
                        'status': 'success',
                        'data': {
                            '_id': books.id,
                            'book_title': books.book_title,
                            'rec_description': books.book_description,
                            'created_on': str(books.created_on),
                            'updated_on': str(books.updated_on)
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

    @validate_request()
    def put(self, id):
        expected = ["book_title", "book_description"]
        # get the post data
        post_data = request.get_json()
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
                books = Books.query.filter_by(id=id).first()
                if not books:
                    return {
                        'status': 'fail',
                        'message': 'No books with the ID'
                    }
                else:
                    for k in post_data.keys():
                        if k not in expected:
                            return {
                                'status': 'fail',
                                'message': k + ' does not exist'
                            }
                    for key, value in post_data.items():
                        if not type(value) == str:
                            return {
                                'status': 'fail',
                                'message': 'Fields must be a string'
                            }
                        if not value.strip():
                            return {
                                'status': 'fail',
                                'message': 'fields can not be empty'
                            }
                        setattr(books, key, value)
                    db.session.add(books)
                    db.session.commit()
                    return {
                        'status': 'success',
                        'message': 'Books Updated successfully'
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

    def delete(self, id):
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
                books = Books.query.filter_by(id=id).first()
                if not books:
                    return {
                        'status': 'fail',
                        'message': 'No Books with the ID'
                    }
                else:
                    db.session.delete(books)
                    db.session.commit()
                    return {
                        'status': 'success',
                        'message': 'Books Deleted successfully'
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
