import os
from flask import Flask, render_template, request, redirect, abort, url_for, make_response, flash
from dotenv import load_dotenv
from io import BytesIO
from gridfs import GridFS
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import requests
from PIL import ImageFile
from numpy import asarray
import pymongo
import certifi

load_dotenv()  # take environment variables from .env.

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
    @app.route('/', methods=['GET'])
    def home():
        return "scrapper"
    @app.route('/scrape', methods=['GET'])
    def scrapeWeb():
        args = request.args
        word = args.get('word')
        # scrape the web, get the result and store them to db then return success if success

        # temp placeholder for testing
        return "1" + word
    @app.route('/wordcloud', methods=['GET'])
    def wordCloud():
        url = "https://en.wikipedia.org/wiki/Meta_Platforms"
        response = requests.get(url)
        soup = BeautifulSoup(response.text,"html.parser")
        text = soup.get_text()
        wordcloud = WordCloud().generate(text)
        image_stream = BytesIO()
        wordcloud.to_image().save(image_stream,format="PNG")
        image_stream.seek(0)
        image_data = image_stream.getvalue()
        image_id = fs.put(image_data)
        db.inputs.insert_one({"name":"meta","text":text,"image_id": image_id})
        return "success"
    return app
app = configure_routes(db = database)

# turn on debugging if in development mode
if os.getenv('FLASK_ENV', 'development') == 'development':
    # turn on debugging, if in development
    app.debug = True # debug mnode

if __name__ == "__main__":
    app.run(debug=True)