import hashlib
import logging
import os

from flask import Flask, session, redirect, request, render_template, make_response

import line
from db import ProfileDAO

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(name)s] %(levelname)s: %(message)s')

app = Flask(__name__)
app.secret_key = 'secret'
db = ProfileDAO()


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/login')
def login():
    access_token = request.cookies.get('token')
    if access_token:
        return redirect('/mypage')

    state = hashlib.sha256(os.urandom(16)).hexdigest()
    session['state'] = state
    url = line.build_login_url(state)
    LOGGER.info(f'redirecting to {url} with state={state}')
    return redirect(url)


@app.route('/callback')
def callback():
    state = request.args.get('state')
    if state != session['state']:
        return f'state mismatch: expected {session["state"]}, but received {state}'
    code = request.args.get('code')

    token_data = line.fetch_token(code)
    if 'access_token' not in token_data:
        return f'access token does not exit: {token_data}'
    access_token = token_data['access_token']

    response = make_response(redirect('/mypage'))
    response.set_cookie('token', access_token)
    return response


@app.route('/mypage')
def mypage():
    access_token = request.cookies.get('token')
    if db.has(access_token):
        profile_data = db.get(access_token)
    else:
        profile_data = line.fetch_profile(access_token)
        db.set(access_token, profile_data)
    return render_template('mypage.html',
                           display_name=profile_data['displayName'],
                           picture_url=profile_data['pictureUrl'])


@app.route('/logout')
def logout():
    access_token = request.cookies.get('token')
    line.revoke_token(access_token)
    db.remove(access_token)
    response = make_response(redirect('/'))
    response.set_cookie('token', '', expires=0)
    return response


if __name__ == "__main__":
    app.run(debug=True)
