import os
import ConfigParser

# DB:
# http://localhost:5984/_utils/

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    config = ConfigParser.RawConfigParser()
    config.read('/home/tracek/.flask/CitizenSensorWeb.cfg')

    SECRET_KEY = config.get('Credentials', 'secret_key')
    ADMIN_USERNAME = config.get('Credentials', 'user')
    ADMIN_PASSWORD = config.get('Credentials', 'password')
    UPLOADED_PHOTOS_DEST = config.get('AppConfig', 'photo_dest')
    DEBUG = config.getboolean('AppConfig', 'debug')
    COUCHDB_SERVER = config.get('AppConfig', 'couchdb_server')
    COUCHDB_DATABASE = config.get('AppConfig', 'couchdb_database')
    PORT = config.getint('AppConfig', 'port')

class ProdConfig(Config):
    HOST = '0.0.0.0'
    PORT = 80

class DevConfig(Config):
    DEBUG = True