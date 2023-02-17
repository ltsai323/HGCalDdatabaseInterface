#!/usr/bin/env python3.10

from xml.etree.ElementTree import Element, tostring
from flask import Flask, request, render_template, redirect, url_for
from flask import json, jsonify
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


@app.route('/home')
def testing():
  return render_template('home.html', text='python powered texts')


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
        'records': {
            'ip_vars': request.form["input_vars"],
            'ip_var2': request.form["input_var2"],
            'ip_var3': request.form["input_var3"],
            'ip_newvar': request.form["input_newvar"],
            'ip_name': request.form["input_name"],
            'ip_email': request.form["input_email"],
            'ip_message': request.form["input_message"],
            'ip_formatter': request.form["input_formatter"],
            'ip_locationid': request.form["input_locationid"],
            'ip_phone': request.form["input_phone"],
            'ip_company': request.form["input_company"],
            'ip_locationid': request.form["input_locationid"],
        },
        'basics': {
            'ip_PART_ID': request.form["input_PART_ID"],
            'ip_KIND_OF_PART_ID': request.form["input_KIND_OF_PART_ID"],
            'ip_LOCATION_ID': request.form["input_LOCATION_ID"],
            'ip_MANUFACTURER_ID': request.form["input_MANUFACTURER_ID"],
            'ip_RECORDED_INSERTION_USER': request.form["input_RECORDED_INSERTION_USER"],
            'ip_BARCODE': request.form["input_BARCODE"],
            'ip_COMMENT_DESCRIPTION': request.form["input_COMMENT_DESCRIPTION"],
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


@app.route('/css/<name>')
def cssFiles(name):
  return redirect(url_for('static', filename=f'css/{name}'))


@app.route('/js/<name>')
def jsFiles(name):
  return redirect(url_for('static', filename=f'js/{name}'))


@app.route('/css/bootstrap/<name>')
def cssbootstrapFiles(name):
  return redirect(url_for('static', filename=f'css/bootstrap/{name}'))


@app.route('/css/bootstrap/mixins/<name>')
def cssbootstrap_mixinsFiles(name):
  return redirect(url_for('static', filename=f'css/bootstrap/mixins/{name}'))


@app.route('/scss/<name>')
def scssFiles(name):
  return redirect(url_for('static', filename=f'scss/{name}'))


@app.route('/scss/bootstrap/<name>')
def scssbootstrapFiles(name):
  return redirect(url_for('static', filename=f'scss/bootstrap/{name}'))


@app.route('/fonts/icommon/<name>')
def fontsFiles(name):
  return redirect(url_for('static', filename=f'fonts/icommon/{name}'))


if __name__ == "__main__":
  app.debug = True
  app.run()

  # 200 伺服器回應Data成功。
  # 206 取得片段資料，Http Request 中有的 Range 屬性，可以指定要取得那一段Bytes數。
  # 301 目標網頁移到新網址(永久轉址)。
  # 302 暫時轉址
  # 304 已讀取過的圖片或網頁，由瀏覽器緩存 (cache) 中讀取。
  # 401 需身分驗證，如 SSL key or htaccess pasword。
  # 403 沒有權限讀取，可能是 IP 被阻檔或是伺服器限制。
  # 404 伺服器未找到目標網址，檔案不存在。
  # 408 Client Request timeout
  # 411 沒有指定 content-length，使用 POST 傳送參數時，必須指定參數的總長度
  # 414 URL 太長導致伺服器拒絕處理。
  # 429 Requests 太多
  # 500 伺服器發生錯誤 : 可能是 htaccess 有錯
  # 503 伺服器當掉 : maybe is code dump
  # 505 不支此 HTTP 版本
