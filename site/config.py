import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SECRE_T_DEFAULT_SECRET_KEY'