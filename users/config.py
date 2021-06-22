#basic configuration of the application

#fetching necessary modules from a seperate .py script
from users.modules import os

#dynamic file path
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    #db file path
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'usermanagement.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'heythisisthesecretkey'