import os,sys
from dotenv import load_dotenv

env_name = os.path.join(os.path.join(os.path.dirname(__file__), '..'),'.env')
if (os.path.exists( env_name )):
    load_dotenv(env_name)
else:
    print (".env file not found.   Exiting");
    sys.exit(1)

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
DEBUG = os.getenv('DEBUG')
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
SECRET_KEY = os.getenv('SECRET_KEY')
REDIS_URI = os.getenv('REDIS_URI')
SESSION_TYPE = os.getenv('SESSION_TYPE')
