#!/usr/bin/env python3.10

from flask import Flask, request, render_template, redirect, url_for
from flask import json, jsonify

app = Flask(__name__)


@app.route('/')
def hello():
  return "Hi the example"


@app.route('/home')
def testing():
  return render_template('test_home.html', text='python powered texts')


@app.route('/form')
def formPage():
  return render_template('test_posterMethod.html')


@app.route('/submit', methods=['POST'])
def submit():
  user = request.form['user']
  print('post : user => ', user)
  return redirect(url_for('success', name=user, action='post'))


@app.route('/<name>')
def user(name):
  return f"Hello {name}"


@app.route('/success/<action>/<name>')
def success(name, action):
  return '{} : Welcome {} ! !!!!!'.format(action, name)


if __name__ == "__main__":
  app.run()
