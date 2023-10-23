import os
import configparser

config = configparser.RawConfigParser(os.environ)
config.read('config.ini')
access_token = config.get('line_api', 'access_token')
secret = config.get('line_api', 'secret')
