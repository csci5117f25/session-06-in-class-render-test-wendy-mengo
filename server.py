from flask import Flask, render_template, request, session, redirect, url_for
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
import db
import os
import json

from dotenv import find_dotenv, load_dotenv
load_dotenv()
load_dotenv(override=True)

app = Flask(__name__)

app.secret_key = app.secret_key = os.environ['FLASK_SECRET']

DATABASE_URL = os.environ.get("DATABASE_URL")
print("DATABASE_URL:", DATABASE_URL)

#db.setup()

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=os.environ.get("AUTH0_CLIENT_ID"),
    client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{os.environ.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)



### auth ###

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect(url_for("hello"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + os.environ.get("AUTH0_DOMAIN") + "/v2/logout?" + urlencode(
            {
                "returnTo": url_for("hello", _external=True),
                "client_id": os.environ.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route('/')
@app.route('/<name>')
def hello(name=None):
    if name:
        session["name"] = name
    return render_template('hello.html', name=name)

@app.route('/data', methods = ['POST'])
def data():
    db.add_person(request.form.get('name'), request.form.get('msg'))
    return render_template('hello.html', name=request.form.get('name'))
