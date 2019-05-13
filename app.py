import os
from flask_bootstrap import Bootstrap
import hashlib
from flask import Flask, render_template, request, redirect, url_for
import json
from pymongo import MongoClient
import gridfs
from vbaparser import vbaparsing
import StringIO
import re

db = MongoClient().myDB
fs = gridfs.GridFS(db)
app = Flask(__name__)
client = MongoClient('localhost', 27017)
db2 = client['Metadata']
Metadata = db2['Metadata'] 


bootstrap = Bootstrap(app)

def md5check(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
        md5sum = hash_md5.hexdigest()
        result = es.search(index="md5", body={"query": {"match": {"IoC": md5sum} }})
    result = json.dumps(result["hits"])
    print(result)
    return result

@app.route('/')
def default():
    return render_template('index.html')

@app.route('/fileupload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        bin_file = StringIO.StringIO(f.read())  
        file_id = fs.put(bin_file,filename=f.filename)
    return str(file_id)


@app.route('/analyse/<md5>')
def analyse_file(md5):
    md5 = str(md5)
    for f in fs.find({"md5": md5}):
    	f = f.read()
    filemdata = {}
    filemdata['md5'] = md5
    #Strings
    result = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", f) 
    filemdata['strings'] = result
    Metadata.insert(filemdata)
    return "test"
