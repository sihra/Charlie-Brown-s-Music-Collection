from flask import Flask
from flask import render_template
import pymongo
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps

app = Flask(__name__)

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27021
DBS_NAME = 'testdb'
COLLECTION_NAME = 'crime'
FIELDS = {'date': True, 'stop-and-search': True, '_id': True}
PARAMETERS = {"date" : "2020-10", "stop-and-search" : [ "Hogwarts"]}
UPDATE = {"_id": {"$oid": "5e98dd1af88346ea89a9d5cd"}}, {"date": "2020-10", "stop-and-search": ["Hogsmeade"]}
DELETE = {"stop-and-search" : [ "Hogwarts"]}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/readCollection")
def readCollection():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    projects = collection.find(projection=FIELDS)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return json_projects

@app.route("/insertCollection")
def insertCollection():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    doc = collection.insert(PARAMETERS)
    projects = collection.find(projection=FIELDS)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return json_projects
    
@app.route("/updateCollection")
def updateCollection():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    doc = collection.update(UPDATE)
    projects = collection.find(projection=FIELDS)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return json_projects

@app.route("/deleteCollection")
def deleteCollection():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    doc = collection.deleteOne(DELETE)
    projects = collection.find(projection=FIELDS)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return json_projects

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)