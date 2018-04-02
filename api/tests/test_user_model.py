import unittest

from api import db
from api.models.user import User
from api.tests.base import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        user = User(
            email='test@test.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
      user = User(
          email='test@test.com',
          password='test'
      )
      db.session.add(user)
      db.session.commit()
      auth_token = user.encode_auth_token(user.id)
      decoded = User.decode_auth_token(auth_token)
      self.assertTrue(isinstance(auth_token, bytes))
      self.assertTrue(decoded['sub']== 1)

if __name__ == '__main__':
    unittest.main()