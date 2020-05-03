from flask import Flask
from flask import render_template
#from flask import request
#from flask import jsonify
import pymongo
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps
from bson import ObjectId

app = Flask(__name__)

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27021
DBS_NAME = 'yelp'
COLLECTION_NAME = 'yelp'
FIELDS = {'user_id': True, 'name': True, 'review_count': True, 'yelping_since': True, 'useful': True, 'funny': True, 'cool': True, 'elite': True, 'friends': True, 'fans': True, 'average_stars': True, 'compliment_hot': True, 'compliment_more': True, 'compliment_profile': True, 'compliment_cute': True, 'complement_list': True, 'compliment_not': True, 'copmliment_plain': True, 'compliment_cool': True, 'compliment_funny': True, 'compliment_writer': True, 'compliment_note': True}
PARAMETERS = {"date" : "2020-10", "stop-and-search" : [ "Hogwarts"]}
#UPDATE = {"stop-and-search" : [ "Hogwarts"]}, {"date": "2020-10", "stop-and-search": ["Hogsmeade"]}, upsert:True, multi:True
#DELETE = {"_id": ObjectId("5e98dd1af88346ea89a9d5cd")}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/readCollection")
def readCollection():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    projects = collection.find(projection=FIELDS).limit(10)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return json_projects

@app.route("/insertCollection")
def insertCollection():
    #insert_name = request.form['insert_name']
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    doc = collection.insert({"name":"Charlie Brown 157C", "review_count": 100})
    #projects = collection.find(projection=FIELDS)
    projects = collection.find({"name":"Charlie Brown 157C"}, {'user_id': 1, 'name': 1, 'review_count': 1, 'yelping_since': 1, 'useful': 1, 'funny': 1, 'cool': 1, 'elite': 1, 'friends': 1, 'fans': 1, 'average_stars': 1, 'compliment_hot': 1, 'compliment_more': 1, 'compliment_profile': 1, 'compliment_cute': 1, 'complement_list': 1, 'compliment_not': 1, 'copmliment_plain': 1, 'compliment_cool': 1, 'compliment_funny': 1, 'compliment_writer': 1, 'compliment_note': 1}).limit(10)
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
    #doc = collection.update({"name" : "Charlie Brown 157C"}, {"review_count": 101})
    doc = collection.update_one({"name": "Charlie Brown 157C"}, {"$set": {"review_count": 101}})
    projects = collection.find({"name":"Charlie Brown 157C"}).limit(10)
    #projects = collection.find({}, {'name': 1}, {$limit:10})
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
    doc = collection.remove({"name" : "Charlie Brown 157C"})
    projects = collection.find({"name":"Charlie Brown 157C"}).limit(10)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return json_projects

@app.route("/findPopularUser")
def findTina():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    projects = collection.find({"fans": {"$gte": 1000}},{"_id" : 0, "name": 1, "fans": 1}).sort([("fans", pymongo.DESCENDING)]).limit(10)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return json_projects

# User Specified: (2) user_id (String > Object ID) >> Return __Name__ has not/been friends with __Name__ for __Years__
# Query: Find if a user specified Yelp user is a friend of another user specified Yelp user
@app.route("/findRelationship")
def findTina():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    projects = collection.find({"fans": {"$gte": 1000}},{"_id" : 0, "name": 1, "fans": 1}).sort([("fans", pymongo.DESCENDING)]).limit(10)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return json_projects

# User Specified: (User Option) Less than, greater than, equal to (User Specified Integer) amount of friends.
# Query: Find users with more than a user specified amount of friends or less than a user specified amount of friends
# Stack Overflow for HTML User Input: https://stackoverflow.com/questions/11556958/sending-data-from-html-form-to-a-python-script-in-flask
@app.route('/findFriendAmount', methods=['GET', 'POST'])
def findFriendAmount():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    
    friendAmount = request.form['friendAmount']
    select = request.form.get('select_friend')

    # Define projects to fill query based on >, <, or ==
    projects = []  

    if(select == "eq"):
        projects = collection.find({"friends": {"$eq": friendAmount}},{"_id" : 0, "name": 1, "friends": 1}).sort([("friends", pymongo.DESCENDING)]).limit(20)
    elif(select == "lt"):
        projects = collection.find({"friends": {"$lt": friendAmount}},{"_id" : 0, "name": 1, "friends": 1}).sort([("friends", pymongo.DESCENDING)]).limit(20)
    else:
        projects = collection.find({"friends": {"$gt": friendAmount}},{"_id" : 0, "name": 1, "friends": 1}).sort([("friends", pymongo.DESCENDING)]).limit(20)

    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return json_projects

yelp.find({"friends": {"$gt": friendAmount}},{"_id" : 0, "name": 1, "friends": 1}).limit(20)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)