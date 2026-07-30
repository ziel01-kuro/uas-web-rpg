import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host':     os.environ.get('DB_HOST', 'localhost'),
    'port':     int(os.environ.get('DB_PORT', 3306)),
    'user':     os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'web_rpg'),
}

SECRET_KEY = os.environ.get('SECRET_KEY', 'ganti-dengan-random-string-sebelum-deploy')

class Config:
    # config database MySQL
    HOST = DB_CONFIG['host']
    PORT = DB_CONFIG['port']
    USER = DB_CONFIG['user']
    PASSWORD = DB_CONFIG['password']
    DATABASE = DB_CONFIG['database']

    # secret Key Flask
    SECRET_KEY = SECRET_KEY

    # config Flask
    DEBUG = os.environ.get("FLASK_DEBUG", "False") == "True"