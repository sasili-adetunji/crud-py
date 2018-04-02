import unittest

from api import db
from api.models.books import Books
from api.tests.base import BaseTestCase


class TestRecordsModel(BaseTestCase):

    
    def setUp(self):
        db.drop_all()
        db.create_all()

        self.book1 = Books(
            book_title='Geography',
            book_description = 'Description of geography'
        )
        self.book2 = Books(
            book_title='ECG',
            book_description='Decsription of ECG of the patient'
        )
        db.session.add(self.book1)
        db.session.commit()
    def test_record_model(self):
        book1_query = Books.query.all()
        db.session.add(self.book2)
        book2_query = Books.query.all()
        self.assertEqual(len(book2_query), len(book1_query) + 1)

    def test_update_record(self):
        """
        To test successful record update.
        """
        # fetch a record
        book = Books.query.filter_by(id=self.book1.id).first()
        # save original description
        old_book_description = book.book_description
        new_book_description = "A new approach Test"
        # update record descrciption
        book.book_description = new_book_description
        db.session.add(book)
        self.assertNotEqual(old_book_description, new_book_description)
        self.assertEqual(book.book_description, "A new approach Test")

if __name__ == '__main__':
    unittest.main()