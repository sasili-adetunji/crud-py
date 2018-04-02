from api import bcrypt, app
from flask import request, make_response, jsonify
from functools import wraps


def hash_pwd(password):
    return bcrypt.generate_password_hash(password, app.config.get('BCRYPT_LOG_ROUNDS')).decode()

def validate_type(item, input_type):
    return type(item) is input_type

def validate_request(*expected_args):
    def real_validate_request(f):
        type_map = {"str": "string",
                    "list": "list",
                    "dict": "dictionary",
                    "int": "integer"}
        @wraps(f)
        def decorated(*args, **kwargs):
            if not request.json:
                return {
                        "status": "fail",
                        "message": "Request must be a valid JSON"
                    }
            payload = request.get_json()
            if payload:
                for values in expected_args:
                    for value in values:
                        if value == values[0]:
                            continue
                        if value not in payload or ((
                                values[0] != dict and not payload[value])):
                            return {
                                "status": "fail",
                                "message": value + " is required"
                            }
                        elif not validate_type(payload[value], values[0]) or not payload[value].strip(
                            ' '):
                            return  {
                                "status": "fail",
                                "message": value + " must be a valid " +
                                         type_map[ values[0].__name__]
                                }
            return f(*args, **kwargs)
        return decorated
    return real_validate_request
