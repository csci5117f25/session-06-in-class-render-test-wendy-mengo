from flask import Flask, render_template, request
import db

app = Flask(__name__)

db.setup

@app.route('/')
@app.route('/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/data', method = ['POST'])
def data():
    db.add_person(request.form.get['name'], request.form.get['msg'])
    return render_template('hello.html', name=request.form['name'])
