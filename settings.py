import configparser

config = configparser.ConfigParser()
config.read('config.ini')
access_token = config['line']['access_token']
secret = config['line']['secret']
