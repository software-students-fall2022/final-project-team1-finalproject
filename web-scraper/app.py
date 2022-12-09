import os
from flask import Flask, render_template, request, redirect, abort, url_for, make_response, flash
import webscraper as webscraper
from dotenv import load_dotenv
import pymongo
from gridfs import GridFS
from wordcloud import WordCloud
from PIL import ImageFile
from numpy import asarray
from io import BytesIO
import math

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

def store_text(db,word,text):
    found = db.inputs.find_one({"word":word})
    if found:
        prev_string = found["text"]
        filter = {"word":word}
        new_string = prev_string + " " + text
        new_values = {"$set":{"text":new_string}}
        db.inputs.update_one(filter,new_values)
        return found["_id"]
    else:
        return db.inputs.insert_one({"word":word,"text":text}).inserted_id

def generate_store_wordcloud(db,id):
    found = db.inputs.find_one({"_id": id})
    text = found["text"]
    # print(text)
    wordcloud = WordCloud(background_color="white", max_words=100,random_state=42,collocations=False).generate(text)
    image_stream = BytesIO()
    wordcloud.to_image().save(image_stream,format="PNG")
    image_stream.seek(0)
    image_data = image_stream.getvalue()
    image_id = fs.put(image_data)
    filter = {"_id": id}
    new_values = {"$set":{"image_id":image_id}}
    db.inputs.update_one(filter,new_values)

def dictionary_convert(dict):
    longStr = ""
    for key in dict:
        i = 0
        freq = dict[key]
        while i < freq:
            longStr = longStr + key + " "
            i = i + 1
    
    return longStr



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
        result = webscraper.WebScrapeProcedures.procedure_1(word)
        
        # allWords = ",".join(list(result.keys()))

        allWords = dictionary_convert(result)
        # allWords = allWords[0:10000]
        #stores text to db, if it is a new word itll insert the text, if it is a word
        #that is previously in the db itll concatinate the text
        stored_id = store_text(db,word,allWords)
        generate_store_wordcloud(db,stored_id)
        #return allWords
        #instead of returning the words it will retrieved the id of the stored document
        return allWords

    return app

app = configure_routes(db = database)

# turn on debugging if in development mode
if os.getenv('FLASK_ENV', 'development') == 'development':
    # turn on debugging, if in development
    app.debug = True # debug mnode

if __name__ == "__main__":
    app.run(debug=True)