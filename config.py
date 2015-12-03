import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    SECRET_KEY = 'barzo trudny tekscik'
    UPLOADED_PHOTOS_DEST = '/tmp/photolog'
    ADMIN_USERNAME = 'quark'
    ADMIN_PASSWORD = 'Charm1974'
    COUCHDB_SERVER = 'http://localhost:5984/'
    COUCHDB_DATABASE = 'flask-photolog'
    PORT = 5000

class ProdConfig(Config):
    HOST = '0.0.0.0'
    PORT = 80

class DevConfig(Config):
    DEBUG = True