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

# connect to the database
database = None
cxn = pymongo.MongoClient(os.getenv('MONGO_URI'), serverSelectionTimeoutMS=5000)
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
        # send request to the web scraper, this will add the input word to the db and store scraped text and wordcloud
        requests.get('http://scraper:5000/scrape', params=payload)
        found = db.inputs.find_one({"word":word})
        image_id= found["image_id"]
        input = found["word"]
        image= fs.get(image_id)

        base64_data = codecs.encode(image.read(), 'base64')
        image = base64_data.decode('utf-8')

        return render_template("home.html",image = image, input=input)
    
    @app.route('/featured')
    def featured():
        found = db.inputs.aggregate([{"$sample" : {"size": 5}}])
        image_ids = []
        inputs = []
        for image in found:
            image_ids.append(image["image_id"])
            inputs.append(image["word"])
        
        fs_images = []
        for id in image_ids:
            fs_images.append(fs.get(id))
        
        images =[]
        for image in fs_images:
            base64_data = codecs.encode(image.read(), 'base64')
            image = base64_data.decode('utf-8')
            images.append(image)
            
        
            
        return render_template("featured.html", images_inputs = zip(inputs,images))
    
    @app.route('/history')
    def history():
        return render_template("history.html")
    return app

app = configure_routes(db = database)

# turn on debugging if in development mode
if os.getenv('FLASK_ENV', 'development') == 'development':
    # turn on debugging, if in development
    app.debug = True # debug mnode

if __name__ == "__main__":
    app.run(debug=True)