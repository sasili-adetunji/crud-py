import unittest
import json
import time

from api import db
from api.models.books import Books

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


class TestRecordsBlueprint(BaseTestCase):
    def setUp(self):

        db.drop_all()
        db.create_all()
        resp_register = register_user(self, 'joe@gmail.com', '123456')
        res = json.loads(resp_register.data.decode())
        resp_login = login_user(self, 'joe@gmail.com', '123456')
  
        books=Books(
          book_title='cardiac',
          book_description='heart problem',
      )

        db.session.add(books)
        db.session.commit()

    def test_valid_post_records(self):
        """ Test for post records """
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.post(
                '/api/v1/book/',
                data=json.dumps(dict(
                    book_description='description of the records',
                    book_title='Title of the records',
                )),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Books Successfully recorded.')
            self.assertTrue(response.content_type == 'application/json')

    def test_invalid_post_records(self):
        """ Test for records without a title"""
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.post(
                '/api/v1/book/',
                data=json.dumps(dict(
                    book_description='description of the records',
                )),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'book_title is required')
            self.assertTrue(response.content_type == 'application/json')

    def test_post_records_without_token(self):
        """ Test for records without a token"""
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.post(
                '/api/v1/book/',
                data=json.dumps(dict(
                    book_description='description of the records',
                    book_title='the ttile of the records',
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide a valid auth token.')
            self.assertTrue(response.content_type == 'application/json')

    def test_post_labortaory_with_malformed_token(self):
        """ Test for laboratiory with malformed token"""
        with self.client:
          resp_login = login_user(self, 'joe@gmail.com', '123456')
          response = self.client.post(
              '/api/v1/book/',
              data=json.dumps(dict(
                    book_description='description of the records',
                    book_title='the title of the records',
                )),
              content_type='application/json',
              headers=dict(
                  Authorization='Bearer' + json.loads(
                      resp_login.data.decode()
                  )['auth_token']
              )
          )
          data = json.loads(response.data.decode())
          self.assertTrue(data['status'] == 'fail')
          self.assertTrue(data['message'] == 'Bearer token malformed.')

    def test_valid_post_existing_records(self):
        """ Test for records already exist"""
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.post(
                '/api/v1/book/',
                data=json.dumps(dict(
                  book_title='cardiac',
                  book_description='heart problem',
                )),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Books already exists.')
            self.assertTrue(response.content_type == 'application/json')

    def test_valid_post_laboratory_with_invalid_token(self):
        """ Test for post laboratory with invalid token """
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.post(
                '/api/v1/book/',
                data=json.dumps(dict(
                    book_description='the test description',
                    book_title='the records title',
                )),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + 'KSNDLVLHIL87327980287'
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Invalid token. Please log in again.')
            self.assertTrue(response.content_type == 'application/json')

    def test_valid_get_records(self):
        """ Test for valid get records """
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.get(
                '/api/v1/book/',
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertIsInstance(data['data']['records'], list)
            self.assertTrue(data['data']['records'][0]['book_description'] == 'heart problem')
            self.assertTrue(response.content_type == 'application/json')

    def test_valid_get_specific_records_that_do_not_exist(self):
        """ Test for valid get specific records that do not exist """
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.get(
                '/api/v1/book/13',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message']== 'No books with this ID')
            self.assertTrue(response.content_type == 'application/json')

    def test_valid_specific_get_records_with_malformed_bearer_token(self):
        """ Test for valid specific get records with malformed bearer token """
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.get(
                '/api/v1/book/12',
                headers=dict(
                    Authorization='Bearer' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Bearer token malformed.')
            self.assertTrue(response.content_type == 'application/json')

    def test_valid_specific_get_records_with_invalid_token(self):
        """ Test for valid specific get records with malformed bearer token """
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.get(
                '/api/v1/book/12',
                headers=dict(
                    Authorization='Bearer ' + 'JKLJHLJOUI788UHILJL'
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Invalid token. Please log in again.')
            self.assertTrue(response.content_type == 'application/json')

    def test_valid_get_records_without_token(self):
        """ Test for valid get records without a token"""
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.get(
                '/api/v1/book/',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide a valid token.')
            self.assertTrue(response.content_type == 'application/json')

    def test_get_records_with_invalid_token(self):
        """ Test for get records with invalid token"""
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.get(
                '/api/v1/book/',
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + 'LSKJVBEWILJO;P984U'
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Invalid token. Please log in again.')
            self.assertTrue(response.content_type == 'application/json')

    def test_get_records_with_malformed_token(self):
        """ Test for get records with malformed token """
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.get(
                '/api/v1/book/',
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Bearer token malformed.')
            self.assertTrue(response.content_type == 'application/json')

    def test_valid_specific_get_records(self):
        """ Test for valid specific get records """
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.get(
                '/api/v1/book/1',
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data']['book_title'] == 'cardiac')
            self.assertTrue(response.content_type == 'application/json')

    def test_valid_specific_get_records_without_token(self):
        """ Test for valid specific get records without token """
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.get(
                '/api/v1/book/12',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'], 'Provide a valid token.')
            self.assertTrue(response.content_type == 'application/json')

    def test_valid_specific_put_records(self):
        """ Test for valid specific put records"""
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.put(
                '/api/v1/book/1',
                data=json.dumps(dict(
                    book_description='emergency heart problem'
                )),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Books Updated successfully')
            self.assertTrue(response.content_type == 'application/json')

    def test_valid_specific_put_records_with_malformed_token(self):
        """ Test for valid specific put records with malformed token"""
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.put(
                '/api/v1/book/1',
                data=json.dumps(dict(
                    rec_description='tooth care description'
                )),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Bearer token malformed.')
            self.assertTrue(response.content_type == 'application/json')

    def test_valid_specific_put_records_without_auth_header(self):
        """ Test for valid specific put laboratory without header """
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.put(
                '/api/v1/book/1',
                data=json.dumps(dict(
                    book_description='tooth care description'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide a valid auth token.')
            self.assertTrue(response.content_type == 'application/json')

    def test_valid_specific_put_records_with_empty_string(self):
        """ Test for valid specific put records with empty string """
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.put(
                '/api/v1/book/1',
                data=json.dumps(dict(
                    book_description='    '
                )),
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'fields can not be empty')
            self.assertTrue(response.content_type == 'application/json')

    def test_valid_specific_put_records_without_string(self):
        """ Test for valid specific put records without string """
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.put(
                '/api/v1/book/1',
                data=json.dumps(dict(
                    book_description=877655
                )),
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Fields must be a string')
            self.assertTrue(response.content_type == 'application/json')

    def test_valid_specific_put_records_with_invalid_token(self):
        """ Test for valid specific put records with invalid token """
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.put(
                '/api/v1/book/1',
                data=json.dumps(dict(
                    book_description=877655
                )),
                headers=dict(
                    Authorization='Bearer ' + 'HAKLSJAS;W943088WJ'
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Invalid token. Please log in again.')
            self.assertTrue(response.content_type == 'application/json')

    def test_valid_specific_put_records_with_a_nonexisting_field(self):
        """ Test for valid specific put records with a non existing field """
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.put(
                '/api/v1/book/1',
                data=json.dumps(dict(
                    book_descriptio="tooth care test description"
                )),
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'book_descriptio does not exist')
            self.assertTrue(response.content_type == 'application/json')

    def test_valid_specific_put_records_that_do_not_exist(self):
        """ Test for valid specific records update that do not exist """
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.put(
                '/api/v1/book/13',
                data=json.dumps(dict(
                    book_description="tooth care description"
                )),
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] ==  'No books with the ID')
            self.assertTrue(response.content_type == 'application/json')

    def test_valid_specific_delete_records_that_do_not_exist(self):
        """ Test for valid specific records delete billing that do not exist """
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.delete(
                '/api/v1/book/13',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'No Books with the ID')
            self.assertTrue(response.content_type == 'application/json')

    def test_valid_specific_delete_records_successfully(self):
        """ Test for valid specific records delete successfully """
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.delete(
                '/api/v1/book/1',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Books Deleted successfully')
            self.assertTrue(response.content_type == 'application/json')

    def test_valid_specific_delete_records_with_malformed_token(self):
        """ Test for valid specific records delete with malformed token """
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.delete(
                '/api/v1/book/12',
                headers=dict(
                    Authorization='Bearer' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Bearer token malformed.')
            self.assertTrue(response.content_type == 'application/json')

    def test_valid_specific_delete_records_without_auth_header(self):
        """ Test for valid specific records delete with malformed token """
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.delete(
                '/api/v1/book/12',
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide a valid auth token.')
            self.assertTrue(response.content_type == 'application/json')

    def test_valid_specific_delete_records_with_invalid_token(self):
        """ Test for valid specific records delete with invalid token """
        with self.client:
            resp_login = login_user(self, 'joe@gmail.com', '123456')
            response = self.client.delete(
                '/api/v1/book/12',
            headers=dict(
                    Authorization='Bearer ' + 'HLJDSHHOL988-78YHJC'
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Invalid token. Please log in again.')
            self.assertTrue(response.content_type == 'application/json')

if __name__ == '__main__':
    unittest.main()