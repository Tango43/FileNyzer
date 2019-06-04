import os
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, redirect, url_for
import json
import pymongo
from pymongo import MongoClient
import gridfs
import StringIO
import sys
from bson import json_util
sys.path.insert(0, 'analysers')
from strings import findip
from yarascan import yaramatch


db = MongoClient().myDB
fs = gridfs.GridFS(db)
app = Flask(__name__)
client = MongoClient('localhost', 27017)
db2 = client['Metadata']
Metadata = db2['Metadata'] 
db3 = client['myDB']

bootstrap = Bootstrap(app)

@app.route('/')
def default():
    report = json_util.dumps(db3['fs.files'].find())
    report = json.loads(report)
    return render_template('index.html',report=report)

@app.route('/upload')
def fileupload():
    return render_template('upload.html')

@app.route('/api/fileupload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        bin_file = StringIO.StringIO(f.read())  
        file_id = fs.put(bin_file,filename=f.filename)
    return redirect(url_for('default'))

@app.route('/inspectfile/<md5>')
def inspect_file(md5):
    md5 = str(md5)
    files = Metadata.find({"md5": md5})
    files = json_util.dumps(files)
    return str(files)

@app.route('/api/analyse/<md5>')    
def analyse_file(md5):
    md5 = str(md5)
    for f in fs.find({"md5": md5}):
    	f = f.read()
    filemdata = {}
    filemdata['md5'] = md5
    #Strings
    ip = findip(f)
    #Yara Match
    yara = yaramatch(f)
    filemdata['strings'] = {}
    filemdata['strings']['ip'] = ip
    filemdata['yara-match'] = []
    for match in yara:
        filemdata['yara-match'].append(match.rule)
    


    Metadata.insert(filemdata)
    return redirect(url_for('inspect_file',md5=md5))
