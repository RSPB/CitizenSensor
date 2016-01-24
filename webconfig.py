import os
import configure

# DB:
# http://localhost:5984/_utils/

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    config = configure.read_config()

    DEBUG = config['Debug']
    SECRET_KEY = config['Credentials']['secret_key']
    ADMIN_USERNAME = config['Credentials']['user']
    ADMIN_PASSWORD = ['Credentials']['password']
    UPLOADED_PHOTOS_DEST = config['AppConfig']['photo_dest']
    COUCHDB_SERVER = config['AppConfig']['couchdb_server']
    COUCHDB_DATABASE = config['AppConfig']['couchdb_database']
    PORT = config['AppConfig']['port']

class ProdConfig(Config):
    HOST = '0.0.0.0'
    PORT = 80

class DevConfig(Config):
    DEBUG = True