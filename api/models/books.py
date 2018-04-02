from api import db
import datetime


class Books(db.Model):
    """ Books Model for storing book related details """
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(255), nullable=False)
    book_description = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_on = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    def __init__(self, book_title, book_description):
        self.book_title = book_title
        self.book_description = book_description
