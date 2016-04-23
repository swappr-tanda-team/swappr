from flask_oauthlib.client import OAuth
from flask import session
from swappr import app

oauth = OAuth(app)
tanda_auth = oauth.remote_app(
    'tanda',
    base_url='https://my.tanda.co/api/v2/',
    request_token_url=None,
    request_token_params={'scope': 'me roster timesheet user cost'},
    access_token_url='https://my.tanda.co/api/oauth/token',
    authorize_url='https://my.tanda.co/api/oauth/authorize',
    app_key='TANDA'
)


@tanda_auth.tokengetter
def get_token():
    if 'tanda_oauth' in session:
        resp = session['tanda_oauth']
        return resp['access_token'], None


# IMPLEMENT API METHODS BELOW HERE

def get_users():
    return tanda_auth.get('users').data
