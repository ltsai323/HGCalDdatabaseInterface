#!/usr/bin/env python3.10

from flask import json, jsonify
from flask import Flask, request, render_template, redirect, url_for
from xml.etree.ElementTree import Element, tostring
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired,Optional, Email

from flask import flash
from flask import json, jsonify
import os
#  BooleanField
#  DateField
#  DateTimeField
#  DecimalField
#  FileField
#  HiddenField
#  MultipleField
#  FieldList
#  FloatField
#  FormField
#  IntegerField
#  PasswordField
#  RadioField
#  SelectField
#  SelectMultipleField
#  SubmitField
#  StringField
#  TextAreaField
#  
#  DataRequired
#  Email
#  EqualTo
#  InputRequired
#  IPAddress
#  Length
#  MacAddress
#  NumberRange
#  Optional
#  Regexp
#  URL
#  UUID
#  AnyOf
#  NoneOf


def __debugging__(*args): print('[debug] - ', *args)
def __no_output__(*args): pass

myLOG = __debugging__


app = Flask(__name__)
Bootstrap(app)

# Create a Form Class
app.config['SECRET_KEY'] = "!!404NotFound!!"

class InputEntry:
    ## in_***.json content
    def __init__(self, iDICT):
        self._var_ = iDICT['_var_']
        self.input = iDICT['input'].lower()
        self.label = InputEntry.GetAttr(iDICT,'label')
        self.check = InputEntry.GetAttr(iDICT,'check')
        self.items = InputEntry.GetAttr(iDICT,'items')
        if self.items: self.items.insert(0, ' -- ') ## first is nothing
    @staticmethod
    def GetAttr(iDICT,name):
        # prevent put error if variable is not found
        return iDICT[name] if name in iDICT else ''
    def Name(self): return self._var_

def DynamicForm(dbITEMS, *args, **kwargs):
    ## Dynamic form is only dynamic at creation. Indeed it is a FlaskForm.
    ## So the flexiblity is only at the constructor

    def Validators(checkList):
        if isinstance(checkList,str): return [Optional()]
        if len(checkList) == 0: return [Optional()]
        if checkList[0] == '': return [Optional()]

        validators = []
        for check in checkList:
            if check == 'data': validators.append( DataRequired() )
            if check == 'email': validators.append( Email(message='EMAIL!!!') )
        return validators

        #def SendError(self, varname):
        #    raise IOError('input %s "%s" is unacceptable. Please Check.' % (varname, getattr(self,varname)))
    def ButtonFactory(inputENTRY:InputEntry):
        if inputENTRY.input == 'str'  : return StringField(inputENTRY.label, validators = Validators(inputENTRY.check))
        if inputENTRY.input == 'email': return StringField(inputENTRY.label, validators = Validators(inputENTRY.check))
        if inputENTRY.input == 'menu' : return SelectField(inputENTRY.label, validators = Validators(inputENTRY.check),
                                                       choices=[(i,l) for i,l in enumerate(inputENTRY.items)])
        return StringField(inputENTRY.label, validators = Validators(inputENTRY.check))
        # end of button factory

    ## create a DBForm
    class MyDBForm(FlaskForm):
        submit = SubmitField("Submit")
        def Get(self, n):
            return getattr(self, n)


    # start point of Dynamic Form
    for itemDict in dbITEMS:
        entry = InputEntry(itemDict)
        setattr( MyDBForm, entry._var_, ButtonFactory(entry) )
        myLOG( 'var : %s has been set!' % itemDict['_var_'] )
    return MyDBForm(*args, **kwargs)



@app.route('/')
def homepage():
  return render_template('homepage.html')
@app.route('/user/<name>')
def helloUsr(name):
    return render_template('test_userHello.html', user_name = name)

# loaded file {{{
@app.route('/assets/dist/css/<name>')
def cssDistFiles(name):
  return redirect(url_for('static', filename=f'assets/dist/css/{name}'))


@app.route('/assets/dist/js/<name>')
def jsDistFiles(name):
  return redirect(url_for('static', filename=f'assets/dist/js/{name}'))

@app.route('/css/<name>')
def cssFiles(name):
  return redirect(url_for('static', filename=f'css/{name}'))


@app.route('/js/<name>')
def jsFiles(name):
  return redirect(url_for('static', filename=f'js/{name}'))

@app.errorhandler(404)
def pagenotfound(e):
    return render_template('404notfound.html')


@app.route('/home')
def home():
  return render_template('home_.html')
# loaded file end }}}



class JsonIOHub:
    def __init__(self):
        self._data = []
    def AppendDataFrom(self, infilename_):
        myLOG('container = %s. new content : %s'%(repr(self._data),repr(JsonIOHub.readjson(infilename_))))
        self._data.extend( JsonIOHub.readjson(infilename_) )

    def WriteAllDataTo(self, outfilename_):
        with open(outfilename_,'w') as ofile:
            json.dump(self._data, ofile, indent=2)

    @property
    def data(self):
        return self._data
    @staticmethod
    def readjson(infilename_) -> list:
        if not os.path.isfile(infilename_): return []
        with open(infilename_,'r') as ifile:
            output = json.load(ifile)
            if isinstance(output, list): return output
            raise IOError('Input json file in invalid format')
    def Save(self, form:DynamicForm):
        self._data = form.data

class GetEntry:
    def __init__(self, indict_):
        self.name = indict_['_var_']
        self.val = indict_['val']



def webInDynamicForm(name, loadedVars:JsonIOHub):
    dataLIST = loadedVars.data

    form = DynamicForm(dataLIST)
    nametypes = [ (entry['_var_'],entry['input']) for entry in dataLIST ]

    myLOG('Old Data @ %s: %s'%(name,form.data))

    suc = None
    # validate form
    if form.validate_on_submit():
        suc = 'hi'
        flash('Form Submitted Successfully')
        myLOG('New Data @ %s: %s'%(name,form.data))

        # open a json to record result
        rec = JsonIOHub()
        rec.Save(form)
        rec.WriteAllDataTo('static/data/out_%s.recorded.json'%name)
    return render_template('%s.html'%name,
                           passed = suc,
                           nametypes = nametypes,
                           form = form)

@app.route('/dev/inventory', methods=['GET','POST'])
def inventory():

    loadedVars = JsonIOHub()
    loadedVars.AppendDataFrom('static/data/in_inventory.json')
    loadedVars.AppendDataFrom('static/data/test_inventory.json')
    return webInDynamicForm('inventory', loadedVars)

@app.route('/dev/assembly', methods=['GET','POST'])
def assembly():

    loadedVars = JsonIOHub()
    loadedVars.AppendDataFrom('static/data/in_assembly.json')
    loadedVars.AppendDataFrom('static/data/test_assembly.json')
    return webInDynamicForm('assembly', loadedVars)


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
