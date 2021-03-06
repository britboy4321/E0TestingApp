# SETUP INFO

# Flask

from flask import Flask, render_template, request, redirect, g, url_for, session
from flask_login import LoginManager, login_required, current_user
from flask_login.utils import login_user


# import logging.config

# from loggly.handlers import HTTPSHandler   
# from logging import Formatter
import os, sys
print ("Current working directory : %s" % os.getcwd()    )

# from flask import LoginManager and login required
import requests                     # Import the whole of requests
import json                         # possibly not needed
import os        # Secrets  (local only)
import pymongo   # required for new mongo database  
from datetime import datetime, timedelta   # Needed for Mongo dates for 'older' records seperation
from todo_app.todo import User              #Import simple user class entry
from oauthlib.oauth2 import WebApplicationClient # Security prep work


# import pytest   (Module 3 not completed yet but will need this stuff).  new additions
from todo_app.models.view_model import ViewModel
from todo_app.todo import Todo

app = Flask(__name__)

mongopassword=os.environ["mongopassword"]       # LOCAL running of Mongo

client = pymongo.MongoClient('mongodb+srv://Daveuser123:' + mongopassword + '@cluster0.yiro1.mongodb.net/myFirstDatabase?w=majority')  # For local (non-cloud) running

#client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client.gettingStarted

app.secret_key = os.environ["SECRET_KEY"]

##  Set token for module 13 - loggly    (no need to disable)

LOGGLY_TOKEN = os.environ["LOGGLY_TOKEN"]

#################################
#  LOGIN MANAGER SETUP
#################################
login_manager = LoginManager()
client_id=os.environ["client_id"] 
Clientsecurity = WebApplicationClient(client_id)
LOG_LEVEL=os.environ["LOG_LEVEL"]
@login_manager.unauthorized_handler
def unauthenticated():
    print("Unauthorised, yet!  You need to add your github name to code below (currently only allows Britboy4321 access to 'write' screen)")
#    app.logger.info("Unauthorised, yet.  If you're not Britboy4321 - have you changed app.py so it has your github user name in it (next to britboy4321)?")

    result = Clientsecurity.prepare_request_uri("https://github.com/login/oauth/authorize")

    print(result)
    return redirect(result)

	# Github OAuth flow when unauthenticated

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

print ("Program starting right now") 
mongopassword=os.environ["mongopassword"]           # Secure password
# hardcoded password to go here if necessary                   
#Set up variables we'll be using...  
client = pymongo.MongoClient('mongodb+srv://britboy4321:' + mongopassword + '@cluster0.yiro1.mongodb.net/myFirstDatabase?w=majority')


login_manager.init_app(app)
client_id=os.environ["client_id"]                   # Needed for local (non-cloud) execution
client_secret=os.environ["client_secret"]           # For security


##### COMMENT THE NEXT TWO LINES FOR DIRECT MONGO DB.  LEAVE THEM IN FOR ASURE COSMOS
mongodb_connection_string = os.environ["MONGODB_CONNECTION_STRING"]    # Line 1 of 2 to use Azure Cosmos
client = pymongo.MongoClient(mongodb_connection_string)                #  LINE 2 of 2 to use Azure Cosmos
################################################################################


db = client.gettingStarted              # Database to be used


olddate = (datetime.now() - timedelta(days=5))   # Mongo: Used to hide staff unavailable for more than 5 days in dropdown
olddate=olddate.date()

# olddate = (datetime.now() + timedelta(days=5))  #Uncomment this line to test 'older items'
                                                  # work without having to hang around for 5 days!

print ("Program starting right now")


#  Create the various lists depending on status

@app.route('/', methods = ["GET","PUT"])
@login_required
def index():

    mongosuperlist=[]               # The name of the Mongo OVERALL test list with all items in it  
    mongo_view_model=[]             # The name of the Mongo AVAILABLE test list (section of collection)
    mongo_view_model_doing=[]       # The name of the Mongo OFFSITE test list (section of collection)
    mongo_view_model_done=[]        # The name of the Mongo UNAVAILABLE test list (section of collection)
    mongo_view_model_olddone=[]     # Tests not completed for 5 days+ (long term unavailable) stored here (section of collection) - seperated so they don't clog up site
    mongosuperlist = list(db.newposts.find())





    counter=0                                           
    for mongo_card in mongosuperlist:
        
        #A list of mongo rows from the collection called 'newposts' 
        whatsthestatus=(mongosuperlist[counter]['status'])
        whatsthedate=(mongosuperlist[counter]['mongodate'])      # Need the date to seperate older 'Done'

        whatsthedate = datetime.strptime(whatsthedate, '%d-%m-%Y').date()

        counter=counter+1                                   #Increment as need to get next list item
        if whatsthestatus == "todo":
            mongo_view_model.append(mongo_card)             # Append to the list of 'Mongo tests not started' - ready for the HTML
        elif whatsthestatus == "doing":
            mongo_view_model_doing.append(mongo_card)       # Append to the list of 'Mongo tests in progress' - ready for the HTML
        elif whatsthestatus == "done":

            if whatsthedate > olddate:

                mongo_view_model_done.append(mongo_card)        # Append to list of 'Mongo test completed - recently' - ready for the HTML
            else: 
                mongo_view_model_olddone.append(mongo_card)     # Append to display in 'older Items from tests completed'            
                                                                # note: Invalid or no status won't appear at all

   # print("the current user is:  ")
    print(current_user.name)
    write_permission_user=(current_user.name)
    
    if (write_permission_user == "britboy4321"):            #THIS LINE HAS TO BE ALTERED if you are not britboy4321, and you want to see the indexwrite.html and have permission to add database entries
        current_user_role="writer"
    else:
        current_user_role="reader"

    print("CURRENT USER ROLE:")
    print(current_user_role)                            


    current_date = datetime.today().strftime('%d-%m-%Y')
    user = str(current_user.name).upper()
    if (current_user_role == "writer"):                 # Can now handle multiple users
        return render_template('indexwrite.html',        # If user allowed to write:
        passed_user_info=user,
        passed_items_todo=mongo_view_model,             # Mongo To Do
        passed_items_doing=mongo_view_model_doing,      # Mongo Doing
        passed_items_done=mongo_view_model_done,        # Mongo Done
        passed_items_olddone=mongo_view_model_olddone,   # Old items ready to be displayed elsewhere
        write_permission_userhtml=write_permission_user,
        current_date=current_date
        )
    else:
        return render_template('indexread.html',
        passed_user_info=user,# If user NOT allowed to write - instead go to 'indexread.html' - the 'read only' version of the site:
        passed_items_todo=mongo_view_model,             # Mongo To Do
        passed_items_doing=mongo_view_model_doing,      # Mongo Doing
        passed_items_done=mongo_view_model_done,        # Mongo Done
        passed_items_olddone=mongo_view_model_olddone,   # Old items ready to be displayed elsewhere
        write_permission_user=write_permission_user
        )
    

@app.route('/addmongoentry', methods = ["POST"])
@login_required
def mongoentry():

    write_permission_user=(current_user.name)
    if (write_permission_user == "britboy4321"):                # Currently Hardcoded.  Add other names here if you need write access
        name = request.form['title']
        mongodict={'title':name,'status':'todo', 'mongodate':datetime.now().strftime('%d-%m-%Y') , 'owner' : current_user.name}
        print(mongodict)
        db.newposts.insert_one(mongodict)

    return redirect("/")


@app.route('/change_owner', methods = ["POST"])
@login_required
def update_owner():
 
    write_permission_user=(current_user.name)
    if (write_permission_user == "britboy4321"):
        NewOwner = request.form['owner']
        title = request.form['title']
        NewOwner = str(NewOwner).lower()
        query = { "title": title }
        val = { "$set": { "owner": NewOwner } }
        db.newposts.update_one(query, val)


    return redirect("/")

@app.route('/deleteAllTests', methods = ["POST"])
@login_required
def deleteAll():

    write_permission_user=(current_user.name)
    if (write_permission_user == "britboy4321"):

        db.newposts.delete_many({})
        '''
        NewOwner = request.form['owner']
        title = request.form['title']

        query = { "title": title }
        val = { "$set": { "owner": NewOwner } }
        
        '''

    return redirect("/")




@app.route('/move_to_doing_item', methods = ["PUT","GET","POST"])
@login_required
def move_to_doing_item():           # Called to move an entry to 'doing' or 'MONGO tests in progress'
#     app.logger.info("Mongo entry being moved to doing (also known as tests in progress (on front end))")
    write_permission_user=(current_user.name)
    if (write_permission_user == "britboy4321"):        # Add other names here if you need write access and you are not britboy4321!
        title = request.form['item_title']
        myquery = { "title": title }
        newvalues = { "$set": { "status": "doing" } }
        db.newposts.update_one(myquery, newvalues)
        for doc in db.newposts.find():  
            print(doc)
    return redirect("/")

@app.route('/move_to_done_item', methods = ["PUT","GET","POST"])
@login_required
def move_to_done_item():            # Called to move an entry to 'done'
#     app.logger.info("Mongo entry being moved to done also known as Tests completed (on front end)")
    write_permission_user=(current_user.name)
    if (write_permission_user == "britboy4321"):        # Add other names here if you need write access and you are not britboy4321!
        title = request.form['item_title']
        myquery = { "title": title }
        newvalues = { "$set": { "status": "done" } }
        db.newposts.update_one(myquery, newvalues)
        for doc in db.newposts.find():  
            print(doc)
    return redirect("/")

@app.route('/move_to_todo_item', methods = ["PUT","GET","POST"])
@login_required
def move_to_todo_item():            # Called to move a 'card' BACK to 'Test not started yet' also known as 'to do' (was useful)
#     app.logger.warning("Something went wrong - user decided to moved data entry back to todo - also known as Mongo tests not yet started")  # I want to keep this as WARNING as something is going wrong if done items arn't done!
    write_permission_user=(current_user.name)
    if (write_permission_user == "britboy4321"):        # Add other names here if you need write access and you are not britboy4321!
        title = request.form['item_title']
        myquery = { "title": title }
        newvalues = { "$set": { "status": "todo" } }
        db.newposts.update_one(myquery, newvalues)
        for doc in db.newposts.find():  
            print(doc)
    return redirect("/")

# @app.route('/performsearch', methods = ["PUT","GET","POST"])            # THIS IS NOT USED YET - IT IS HERE FOR SOMETHING I MAY DO IN THE FUTURE.
# def performseach():
#    searchterm = request.form['skillsearch']
#    print("Current Search Term is:")
#    print(searchterm)
 #   return redirect("/")


@app.route('/login/callback', methods = ["GET","POST"])
def login():

    # Get the access_token
    print("ABOUT TO PREPARE THE TOKEN REQUIRED")
    url, headers, body = Clientsecurity.prepare_token_request(
        "https://github.com/login/oauth/access_token",
        authorization_response=request.url
    )

    print("REACHED TOKEN RESPONSE")
    token_response = requests.post(
        url,
        headers=headers,
        data=body,
        auth=(client_id, client_secret)
        )

    # Now to get the users data
    print("Reached parsing into Client security")
    Clientsecurity.parse_request_body_response(token_response.text)
    url, headers, body = Clientsecurity.add_token("https://api.github.com/user")
    print("Reached user_response")    
    user_response = requests.get(url, headers=headers, data=body) 
    the_user_name = user_response.json()['login']
    print("Attempting to login user")
    login_user(User(the_user_name))
    print("Reached return")
    return redirect("/")

if __name__ == '__main__':
   
   app.run()
