from flask import Flask, render_template
from flask import request
# from flask import jsonify
import re
import pymongo
from pymongo import MongoClient
import json
from bson import json_util
from bson.son import SON
from bson.json_util import dumps
from bson import ObjectId

app = Flask(__name__)



MONGODB_HOST = 'localhost'
MONGODB_PORT = 27021
DBS_NAME = 'project'
COLLECTION_NAME = 'project'
FIELDS = {'user_id': True, 'name': True, 'review_count': True, 'yelping_since': True, 'useful': True, 'funny': True,
          'cool': True, 'elite': True, 'friends': True, 'fans': True, 'average_stars': True, 'compliment_hot': True,
          'compliment_more': True, 'compliment_profile': True, 'compliment_cute': True, 'complement_list': True,
          'compliment_not': True, 'copmliment_plain': True, 'compliment_cool': True, 'compliment_funny': True,
          'compliment_writer': True, 'compliment_note': True}
PARAMETERS = {"date": "2020-10", "stop-and-search": ["Hogwarts"]}


# UPDATE = {"stop-and-search" : [ "Hogwarts"]}, {"date": "2020-10", "stop-and-search": ["Hogsmeade"]}, upsert:True, multi:True
# DELETE = {"_id": ObjectId("5e98dd1af88346ea89a9d5cd")}

def makeSureValueIsInt(val, defaultVal):
     try:
        val = int (val)
     except ValueError:
        return defaultVal
     return  val


@app.route("/")
def index():
    return render_template("index.html")

###############################
@app.route("/findReviews", methods=['POST'])  #amount
def findReviews():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    output_amount = makeSureValueIsInt(request.form['reviewOutputAmount'], 10)
    review_amount = makeSureValueIsInt(request.form['numberOfReviews'], 250)
    projects = collection.find({"review_count": {"$gte": review_amount}}, {"_id": 0, "name": 1, "review_count": 1}).sort(
        [("fans", pymongo.ASCENDING)]).limit(output_amount)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()

    return render_template("QueryTemplate.html", json_projects = json_projects)



@app.route("/findUsername", methods =['POST']) #userName, amount
def findUsername():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    output_amount = makeSureValueIsInt(request.form['characterOutputAmount'], 10)
    user_name = request.form['characters']
    projects = collection.find({"name": re.compile(user_name, re.IGNORECASE)}, {"_id" : 0, "name": 1, "yelping_since": 1}).limit(output_amount)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return render_template("QueryTemplate.html", json_projects = json_projects)

@app.route("/findPopularUser", methods = ['POST']) #fansMin, fansMax, amount
def findPopularUsers():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    amount = makeSureValueIsInt(request.form['fansOutputAmount'], 10)
    fansMin = makeSureValueIsInt(request.form['fanMin'], 1)
    fansMax = makeSureValueIsInt(request.form['fanMax'], 10000)
    
    projects = collection.find({"fans": {"$gte": fansMin, "$lte": fansMax}}, {"_id": 0, "name": 1, "fans": 1}).sort(
        [("fans", pymongo.DESCENDING)]).limit(amount)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return render_template("QueryTemplate.html", json_projects=json_projects)

@app.route("/findJoinDate", methods = ['POST']) #date, amount
def findJoinDate():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    amount = makeSureValueIsInt(request.form['dateOutputAmount'], 10)
    date = makeSureValueIsInt(request.form['date'], 2007)
    projects = collection.find({"yelping_since": re.compile(str(date), re.IGNORECASE)}, {"_id" : 0, "name":1, "yelping_since": 1}).limit(amount)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return render_template("QueryTemplate.html", json_projects=json_projects)



@app.route("/findCompliments", methods = ['POST']) #name, amount
def findCompliments():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    radio = request.form['groupOfDefaultRadios']
    amount = makeSureValueIsInt(request.form['complimentOutputAmount'], 10)
    name = request.form['complimentName']
    projects = collection.find({"name" : name},{"_id": 0, "name" : 1, radio: 1}).limit(amount)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return render_template("QueryTemplate.html", json_projects=json_projects)


################## Find Friendship Query ####################
# User Specified: (2) user_id (String > Object ID) >> Return __Name__ has not/been friends with __Name__ for __Years__
# Query: Find if a user specified Yelp user is a friend of another user specified Yelp user
@app.route("/findFriendship", methods=['POST'])
def findFriendship():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]

    userid_one = request.form['user_id_one']
    userid_two = request.form['user_id_two']
    projects = collection.find({"user_id": userid_one},{"_id" : 0, "friends": 1})
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    friends = (str(json_projects)[14:-3]).split(',')
    areTheyFriends = False
    for friend in friends:
        if(friend.strip() == userid_two.strip()):
            areTheyFriends = True    
    json_projectst = []
    projectst = []
    if(areTheyFriends == True):
        projectst = collection.aggregate([
            {'$addFields': {'Relationship_Status': True, 'First_User': userid_one, 'Second_User': userid_two}},
            {"$match" : {"user_id": userid_one}},
            {"$project": { "First_User": 1, "Second_User": 1, "Relationship_Status": 1, "friends": 1}}
        ])
    else:
        projectst = collection.aggregate([
            {'$addFields': {'Relationship_Status': False, 'First_User': userid_one, 'Second_User': userid_two}},
            {"$match" : {"user_id": userid_one}},
            {"$project": { "Second_User": 1, "First_User": 1, "Relationship_Status": 1, "friends": 1}}
        ])
    for project in projectst:
        json_projectst.append(project)
    json_projectst = json.dumps(json_projectst, default=json_util.default)
    connection.close()
    return render_template("QueryTemplate.html", json_projects=json_projectst)


############### Largest Review with Largest Specified Review Average#################
# Query:  Find users with the largest review count and user specified average
@app.route("/findAvg", methods=['POST'])
def findAvg():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]

    avg_review= request.form['avg_review']
    avg_review = float(avg_review)
    projects = collection.find({"average_stars": avg_review},{"_id" : 0, "name": 1, "average_stars": 1, "review_count": 1}).sort([("review_count", pymongo.DESCENDING)]).limit(20)

    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return render_template("QueryTemplate.html", json_projects=json_projects)

############### Find Amount of Friends ##################
# User Specified: (User Option) Less than, greater than, equal to (User Specified Integer) amount of friends.
# Query: Find users with more than a user specified amount of friends or less than a user specified amount of friends
@app.route('/findFriendAmount', methods=['GET', 'POST'])
def findFriendAmount():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]

    friendAmount = int(request.form['friendAmount'])
    select = request.form.get('select_friend')
    friendAmount = int(friendAmount)

    projects = []
    # Define projects to fill query based on >, <, or ==
    if(select == "eq"):
        projects = collection.aggregate([
            {'$addFields': {'Friend_Amount': {"$size": {"$split": ["$friends", ","]}}}},
            {'$match': {'friends': {"$exists": True}, 'Friend_Amount': {"$eq": friendAmount}} },
            {'$project': {'user_id': 1, 'name': 1, 'Friend_Amount': 1}},
            {'$limit': 10 }
        ])
    elif(select == "gt"):
        projects = collection.aggregate([
            {'$addFields': {'Friend_Amount': {"$size": {"$split": ["$friends", ","]}}}},
            {'$match': {'friends': {"$exists": True}, 'Friend_Amount': {"$gt": friendAmount}} },
            {'$project': {'user_id': 1, 'name': 1, 'Friend_Amount': 1}},
            {'$sort': SON([('Friend_Amount', -1)])},
            {'$limit': 10 }
        ])
    elif(select == "lt"):
        projects = collection.aggregate([
            {'$addFields': {'Friend_Amount': {"$size": {"$split": ["$friends", ","]}}}},
            {'$match': {'friends': {"$exists": True}, 'Friend_Amount': {"$lt": friendAmount}} },
            {'$project': {'user_id': 1, 'name': 1, 'Friend_Amount': 1}},
            {'$sort': SON([('Friend_Amount', -1)])},
            {'$limit': 10 }
        ])
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return render_template("QueryTemplate.html", json_projects=json_projects)

####### Most reviews within time of yelping #########
@app.route("/mostReviewYelping")
def mostReviewYelping():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    projects = collection.aggregate([
        {'$addFields': { 'Ratio_Of_Reviews_As_Yelp_Member': {'$divide': ['$review_count', {'$subtract': [ "$$NOW", { '$dateFromString': { 'dateString': '$yelping_since' }}]}]} }},  
        {'$project': { 'name': 1, '_id': 1, 'yelping_since': 1, 'review_count': 1, 'Ratio_Of_Reviews_As_Yelp_Member': 1}}, 
        {'$sort': SON([('Ratio_Of_Reviews_As_Yelp_Member', -1)])},
        {'$limit': 30 } 
    ])
    json_projects = []
    for project in projects:
        json_projects.append(";")
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return render_template("QueryTemplate.html", json_projects=json_projects)


########### find Users who joined in a specific year and how long they've been members ###########
@app.route("/findYearOfYelp", methods=['POST'])  #amount
def findYearOfYelp():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    yearOfYelp = int(request.form['yearOfYelp'])
    projects = collection.aggregate([
        { '$addFields': { 
            'date': { '$dateFromString': { 'dateString': '$yelping_since' }}, 
            'Days_Since_Yelping': {'$subtract': [ "$$NOW", {'$dateFromString':{'dateString': '$yelping_since'}} ]}, 
            'Year': {'$year': {'$dateFromString':{'dateString': '$yelping_since'}}} }},
        {'$match': {'Year': yearOfYelp}}, 
        {'$project': { '_id': 1, 'Year': 1, 'yelping_since': 1, 'Days_Since_Yelping': 1, 'review_count': 1 } }, 
        {'$sort': SON([('Days_Since_Yelping', -1)])},        
        {'$limit': 30} 
    ]) 
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return render_template("QueryTemplate.html", json_projects = json_projects)


##############################
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
    return render_template("QueryTemplate.html", json_projects=json_projects)

@app.route("/insertCollection")
def insertCollection():
    #insert_name = request.form['insert_name']
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    doc = collection.insert({"user_id" : "3893724ru923hfl9","name":"Charlie Brown 157C", "review_count": 100})
    #projects = collection.find(projection=FIELDS)
    projects = collection.find({"name":"Charlie Brown 157C"}, {'user_id': 1, 'name': 1, 'review_count': 1, 'yelping_since': 1, 'useful': 1, 'funny': 1, 'cool': 1, 'elite': 1, 'friends': 1, 'fans': 1, 'average_stars': 1, 'compliment_hot': 1, 'compliment_more': 1, 'compliment_profile': 1, 'compliment_cute': 1, 'complement_list': 1, 'compliment_not': 1, 'copmliment_plain': 1, 'compliment_cool': 1, 'compliment_funny': 1, 'compliment_writer': 1, 'compliment_note': 1}).limit(10)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return render_template("QueryTemplate.html", json_projects=json_projects)
@app.route("/updateCollection")
def updateCollection():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    # doc = collection.update({"name" : "Charlie Brown 157C"}, {"review_count": 101})
    doc = collection.update_one({"name": "Charlie Brown 157C"}, {"$set": {"review_count": 101}})
    projects = collection.find({"name": "Charlie Brown 157C"}).limit(10)
    # projects = collection.find({}, {'name': 1}, {$limit:10})
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return render_template("QueryTemplate.html", json_projects=json_projects)


@app.route("/deleteCollection")
def deleteCollection():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    doc = collection.remove({"name": "Charlie Brown 157C"})
    projects = collection.find({"name": "Charlie Brown 157C"}).limit(10)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return render_template("QueryTemplate.html", json_projects=json_projects)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)