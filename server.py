from flask import Flask, render_template, request, session
import db
import os
from dotenv import load_dotenv
load_dotenv()
load_dotenv(override=True)

app.secret_key = app.secret_key = os.environ['FLASK_SECRET']

DATABASE_URL = os.environ.get("DATABASE_URL")
print("DATABASE_URL:", DATABASE_URL)

app = Flask(__name__)

db.setup

@app.route('/')
@app.route('/<name>')
def hello(name=None):
    if name:
        session["name"] = name
    return render_template('hello.html', name=name)

@app.route('/data', methods = ['POST'])
def data():
    db.setup()
    db.add_person(request.form.get('name'), request.form.get('msg'))
    return render_template('hello.html', name=request.form.get('name'))
