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


def make_connection():
# connect to the database
    load_dotenv()  # take environment variables from .env.
    cxn = pymongo.MongoClient(os.getenv('MONGO_URI'), serverSelectionTimeoutMS=5000,tls=True,tlsAllowInvalidCertificates=True)
    return cxn

def def_db(cxn):
    try:
        # verify the connection works by pinging the database
        cxn.admin.command('ping') # The ping command is cheap and does not require auth.
        database = cxn[os.getenv('MONGO_DBNAME')] # store a reference to the databasex
        print(' *', 'Connected to MongoDB!') # if we get here, the connection worked!
        return database
    except Exception as e:
        # the ping command failed, so the connection is not available.
        print(' *', "Failed to connect to MongoDB at", os.getenv('MONGO_URI'))
        print('Database connection error:', e) # debug
        return -1

def configure_routes():
    # set up a web app with correct routes
    app = Flask(__name__)
    cnx = make_connection()
    db = def_db(cnx)
    fs = GridFS(db)
    @app.route('/')
    def home():
        return render_template("home.html")

    @app.route('/keyword' , methods=['GET'])
    def generate():
        
        args = request.args
        word = args.get('word')

        if (word == ''):
            return render_template("home.html", input="Empty String", inputError="An empty string is not a valid query. Try a different query")
        elif (str(word).isnumeric()):
            return render_template("home.html", input=word, inputError="A query cannot only have numbers. Try a different query")

        requestURL = os.environ['SCRAPE_URL']
        payload = {'word': word}
        # send request to the web scraper, this will add the input word to the db and store scraped text and wordcloud
        requests.get(requestURL, params=payload)
        found = db.inputs.find_one({"word": word})
        image_id = found.get("image_id", None)
        input = found.get("word", None)
        if (image_id != None and input != None):
            image = fs.get(image_id)
            base64_data = codecs.encode(image.read(), 'base64')
            image = base64_data.decode('utf-8')
            return render_template("home.html", image = image, input=input)
        else:
            return render_template("home.html", input=word, inputError=("Unable to generate a wordcloud using the following query: " + input))
        
    
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

app = configure_routes()

# turn on debugging if in development mode
if os.getenv('FLASK_ENV', 'development') == 'development':
    # turn on debugging, if in development
    app.debug = True # debug mnode

if __name__ == "__main__":
    app.run(debug=True)