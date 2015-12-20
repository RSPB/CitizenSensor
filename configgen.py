# Simple module to write config.

import ConfigParser

config = ConfigParser.RawConfigParser()
config.add_section('Credentials')
config.set('Credentials', 'user', 'user')
config.set('Credentials', 'password', 'password')
config.set('Credentials', 'secret_key', 'key')

config.add_section('AppConfig')
config.set('AppConfig', 'photo_dest', 'dest')
config.set('AppConfig', 'couchdb_server', 'server')
config.set('AppConfig', 'couchdb_database', 'db')
config.set('AppConfig', 'port', '42')
config.set('AppConfig', 'debug', 'False')

with open('CitizenSensorWeb.cfg', 'wb') as configfile:
    config.write(configfile)