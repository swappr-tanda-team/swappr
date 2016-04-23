from flask_oauthlib.client import OAuth
from flask import session
from swappr import app
import swappr.god_request
import os

redirect_uri='http://localhost:9000/user/authorize'
if ('REDIRECT_URI' in os.environ):
    redirect_uri=os.environ['REDIRECT_URI']

oauth = OAuth(app)
tanda_auth = oauth.remote_app(
    'tanda',
    base_url='https://my.tanda.co/api/v2/',
    request_token_url=None,
    request_token_params={'scope': 'me roster timesheet user cost', redirect_uri: redirect_uri},
    access_token_url='https://my.tanda.co/api/oauth/token',
    authorize_url='https://my.tanda.co/api/oauth/authorize',
    app_key='TANDA',
    access_token_params={
        redirect_uri:redirect_uri
    }
)


@tanda_auth.tokengetter
def get_token():
    return session.get('oauth_token')


# IMPLEMENT API METHODS BELOW HERE

def get_users():
    return tanda_auth.get('users').data


def get_schedules(ids, show_costs=False):
    return tanda_auth.get('schedules?ids={}&showCosts={}'.format(','.join(ids), show_costs))


def get_managers_for_department(department_id):
    department = swappr.god_request.get('departments/' + str(department_id)).json()
    manager_ids = department["managers"]
    all_users = swappr.god_request.get('users').json()
    managers = []
    for i in range(len(all_users)):
        user = all_users[i]
        if user["id"] in manager_ids:
            managers.append(user)
    return managers

