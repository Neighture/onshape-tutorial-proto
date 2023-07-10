from flask import Flask, url_for, session, request
from flask_cors import CORS
from flask_session import Session
from flask import render_template, redirect
from authlib.integrations.flask_client import OAuth
import json

app = Flask(__name__)
app.config.from_object('config')

Session(app)
CORS(app, supports_credentials=True)

oauth = OAuth(app)
oauth.register(
  name='onshape',
  access_token_url='https://oauth.onshape.com/oauth/token',
  authorize_url='https://oauth.onshape.com/oauth/authorize',
  fetch_token=lambda: session.get('token'),  # DON'T DO IT IN PRODUCTION
)


@app.route('/')
def homepage():
  user = session.get('user')
  doc_id = request.args.get('documentId')
  ele_id = request.args.get('elementId')
  history_type = request.args.get('workspaceOrVersion')
  history_id = request.args.get('workspaceOrVersionId')

  if history_type:
    url = f'https://cad.onshape.com/api/v6/documents/d/{doc_id}/{history_type}/{history_id}/elements?withThumbnails=false'
    resp = oauth.onshape.get(url)
    print(resp.text)

  return render_template('home.html',
                         user=user,
                         doc_id=doc_id,
                         ele_id=ele_id,
                         workspaceOrVersion=history_type,
                         workspaceOrVersionId=history_id)


@app.route('/login')
def login():
  redirect_uri = url_for('auth', _scheme="https", _external=True)
  return oauth.onshape.authorize_redirect(redirect_uri)


@app.route('/auth')
def auth():
  token = oauth.onshape.authorize_access_token()
  resp = oauth.onshape.get('https://cad.onshape.com/api/users/sessioninfo')
  user = resp.json()
  session['user'] = user
  session['token'] = token
  return redirect('/')


@app.route('/logout')
def logout():
  session.pop('user', None)
  session.pop('token', None)
  return redirect('/')


@app.route('/set_session')
def set_session():
  session['test'] = 'foo'
  value = session.get('test')
  print(value)
  return 'set session'


@app.route('/read_session')
def read_session():
  value = session.get('test')
  print(value)
  return "attempted"


@app.route('/partstudio')
def get_partstudio():
  return render_template('partstudio.html')


@app.route('/assemblystudio')
def get_assemblystudio():
  return render_template('assemblystudio.html')


# @token_update.connect_via(app)
# def on_token_update(sender,
#                     name,
#                     token,
#                     refresh_token=None,
#                     access_token=None):
#   if refresh_token:
#     item = OAuth2Token.find(name=name, refresh_token=refresh_token)
#   elif access_token:
#     item = OAuth2Token.find(name=name, access_token=access_token)
#   else:
#     return

#   # update old token
#   item.access_token = token['access_token']
#   item.refresh_token = token.get('refresh_token')
#   item.expires_at = token['expires_at']
#   item.save()

app.run(host='0.0.0.0', debug=True, port=443)

# https://cad.onshape.com/api/v6/documents/d/72c20672f3b938bafc1a3268/w/elements
# https://cad.onshape.com/api/v6/documents/d/72c20672f3b938bafc1a3268/w/02b39b5783b32586f9c7bc2a/elements?withThumbnails=false
# https://cad.onshape.com/api/v6/documents/d/72c20672f3b938bafc1a3268/w/02b39b5783b32586f9c7bc2a/elements
# https://cad.onshape.com/api/v6/documents/d/72c20672f3b938bafc1a3268/w/02b39b5783b32586f9c7bc2a/elements?withThumbnails=false