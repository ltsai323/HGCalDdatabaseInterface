#!/usr/bin/env python3.10

from xml.etree.ElementTree import Element, tostring
from flask import Flask, request, render_template, redirect, url_for
from flask import json, jsonify

app = Flask(__name__)


@app.route('/home')
def testing():
  return render_template('test_home.html', text='python powered texts')


@app.route('/ajaxDemo')
def ajaxdemo():
  return render_template('test_ajaxSimpleDemo.html')


@app.route('/mytest')
def mytest():
  return render_template('test_ajaxDemo.html')


@app.route('/modifiedContactForm')
def newContactForm():
  return render_template('test_modifiedContactForm.html')


@app.route('/data/message', methods=['GET'])
def getDataMessage():
  if request.method.upper() == 'GET':
    with open('static/data/message.json', 'r') as f:
      data = json.load(f)
      print('text : ', data)
    return jsonify(data)


@app.route('/data/message/', methods=['POST'])
def setDataMessage():
  if request.method == "POST":
    data = {
        'appInfo': {
            'name': request.form['name'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'company': request.form['company']
        }
    }
    print(type(data))
    with open('static/data/input.json', 'w') as f:
      json.dump(data, f)
    with open('static/data/input.xml', 'w') as f:
      elem = Element('root')
      for cat, rec in data.items():
        elem_cat = Element(cat)
        for key, val in rec.items():
          sub_elem = Element(key)
          sub_elem.text = str(val)
          elem_cat.append(sub_elem)
        elem.append(elem_cat)
      f.write(tostring(elem, encoding='unicode'))
    return jsonify(result='OK')


@app.route('/success/<action>/<name>')
def success(name, action):
  return '{} : welcome {} !!'.format(action, name)


if __name__ == "__main__":
  app.debug = True
  app.run()
