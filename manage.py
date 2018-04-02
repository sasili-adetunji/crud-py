from flask import Flask, request, jsonify
from api import db, app
from api.models.user import user_schema, users_schema, User
from flask_restful import Api
from api.resource.user_resource import LoginResource, RegisterResource
from api.resource.book_resource import BookResource, BookDetailsResource

api = Api(app)

import os
import unittest
import coverage

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# import pdb;pdb.set_trace()

COV = coverage.coverage(
    branch=True,
    include='api/*',
    omit=[
        'api/tests/*',
        'api/server/config.py',
        'api/server/*/__init__.py'
    ]
)
COV.start()

from api import app, db

migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('api/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('api/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1

@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()

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
    BookResource,
    '/api/v1/book',
    '/api/v1/book/',
    endpoint='books')

api.add_resource(
    BookDetailsResource,
    '/api/v1/book/<string:id>',
    '/api/v1/book/<string:id>/',
    endpoint='book_details')


if __name__ == "__main__":
    manager.run()

