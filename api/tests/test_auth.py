import unittest
import json
import time

from api import db
from api.models.user import User

from api.tests.base import BaseTestCase

def register_user(self, email, password):
    return self.client.post(
        '/api/v1/register/',
        data=json.dumps(dict(
            email=email,
            password=password
        )),
        content_type='application/json',
    )

def login_user(self, email, password):
    return self.client.post(
        '/api/v1/login/',
        data=json.dumps(dict(
            email=email,
            password=password
        )),
        content_type='application/json',
    )

class TestAuthBlueprint(BaseTestCase):
    def setUp(self):

        db.drop_all()
        db.create_all()
        resp_register = register_user(self, 'joe@gmail.com', '123456')
        res = json.loads(resp_register.data.decode())
        resp_login = login_user(self, 'joe@gmail.com', '123456')


    def test_registration(self):
        """ Test for user registration """
        with self.client:
            response = register_user(self, 'joetest@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered. Login with your email')
            self.assertTrue(response.content_type == 'application/json')


    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered email"""
        with self.client:
            response = register_user(self, 'joe@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'This account already exists and active')
            self.assertTrue(response.content_type == 'application/json')

    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        with self.client:
            response = login_user(self, 'joe@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        with self.client:
            response = login_user(self, 'joe@gmail.com', '12345')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Login credentials is incorrect.')
            self.assertTrue(response.content_type == 'application/json')

    def test_decode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test',
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        decode = User.decode_auth_token(auth_token.decode("utf-8"))
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue( decode['sub'] == 2)

    def test_valid_string(self):
        """ Test for valid string"""
        with self.client:
            response = login_user(self, 2222, '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'email must be a valid string')

    def test_nonempty_password(self):
        """ Test for unempty password"""
        with self.client:
            response = login_user(self, 'joe@emailcom', '    ')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'password must be a valid string')

    def test_valid_parameter(self):
        """ Test for valid parameter"""
        with self.client:
            response = self.client.post(
                '/api/v1/login/',
                data=json.dumps(dict(
                    emai='joe@gmail.com',
                    password='123456'
                )),
                content_type='application/json',
            )            
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'email is required')

    def test_valid_json_request(self):
            """ Test for valid JSON request"""
            with self.client:
                response = self.client.post(
                    '/api/v1/login/',
                    data=json.dumps(dict(
                        emai='joe@gmail.com',
                        password='123456'
                    )),
                )            
                data = json.loads(response.data.decode())
                self.assertTrue(data['status'] == 'fail')
                self.assertTrue(data['message'] == 'Request must be a valid JSON')

if __name__ == '__main__':
    unittest.main()