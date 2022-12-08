import os
from flask import Flask, render_template, request, redirect, abort, url_for, make_response, flash
from dotenv import load_dotenv
import requests
import pymongo
from io import BytesIO
from gridfs import GridFS
from PIL import ImageFile
import base64
import codecs
load_dotenv()  # take environment variables from .env.
import certifi

# connect to the database
database = None
cxn = pymongo.MongoClient(os.getenv('MONGO_URI'), serverSelectionTimeoutMS=5000,tlsCAFile=certifi.where())
try:
    # verify the connection works by pinging the database
    cxn.admin.command('ping') # The ping command is cheap and does not require auth.
    database = cxn[os.getenv('MONGO_DBNAME')] # store a reference to the database
    fs = GridFS(database)
    print(' *', 'Connected to MongoDB!') # if we get here, the connection worked!
except Exception as e:
    # the ping command failed, so the connection is not available.
    print(' *', "Failed to connect to MongoDB at", os.getenv('MONGO_URI'))
    print('Database connection error:', e) # debug

def configure_routes(db):
    # set up a web app with correct routes
    app = Flask(__name__)
    @app.route('/')
    def home():
        return render_template("home.html")

    @app.route('/keyword' , methods=['GET'])
    def generate():
        
        args = request.args
        word = args.get('word')
        payload = {'word':word}
        # send request to the web scraper, add the keyword as the query string

  
        #aleoalzabal code
        company = db.inputs.find_one({"name":"meta"})

        image_id= company["image_id"]
        image= fs.get(image_id)

        base64_data = codecs.encode(image.read(), 'base64')
        image = base64_data.decode('utf-8')

        return render_template("home.html",image = image)
        #message = requests.get('http://scraper:5000/scrape', params=payload) 
        #return message.text


    return app

app = configure_routes(db = database)

# turn on debugging if in development mode
if os.getenv('FLASK_ENV', 'development') == 'development':
    # turn on debugging, if in development
    app.debug = True # debug mnode

if __name__ == "__main__":
    app.run(debug=True)