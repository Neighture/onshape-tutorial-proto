import os

STACK = os.environ['STACK']
ONSHAPE_CLIENT_ID = os.environ['ONSHAPE_CLIENT_ID']
ONSHAPE_CLIENT_SECRET = os.environ['ONSHAPE_CLIENT_SECRET']
SECRET_KEY = os.environ['SESSION_SECRET_KEY']
SESSION_TYPE = 'filesystem'

SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True
