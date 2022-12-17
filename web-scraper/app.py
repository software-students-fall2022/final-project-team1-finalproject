import os
from flask import Flask, render_template, request, redirect, abort, url_for, make_response, flash
import webscraper as webscraper
from dotenv import load_dotenv
import pymongo
from gridfs import GridFS
from wordcloud import WordCloud, STOPWORDS
from datetime import datetime
from PIL import ImageFile
from numpy import asarray
from io import BytesIO
import math
import random
import mongomock



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

def store_text(db,word,text):
    found = db.inputs.find_one({"word":word})
    if found:
        filter = {"word":word}
        new_values = {"$set":{"text":text}}
        db.inputs.update_one(filter,new_values)
        return found["_id"]
    else:
        return db.inputs.insert_one({"word":word,"text":text}).inserted_id

def generate_store_wordcloud(db,fs,word,id):
    found = db.inputs.find_one({"_id": id})
    text = found["text"]
    # print(text)
    randomNum = math.floor(random.random()*100)
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color="white", max_words=100, random_state=randomNum,collocations=False,width=1280, height=720).generate(text)
    image_stream = BytesIO()
    wordcloud.to_image().save(image_stream,format="PNG")
    image_stream.seek(0)
    image_data = image_stream.getvalue()
    image_id = fs.put(image_data)
    filter = {"_id": id}
    new_values = {"$set":{"image_id":image_id}}
    db.inputs.update_one(filter,new_values)
    db.history.insert_one({"word":word,"date": datetime.now(),"image_id": image_id})

    # Benji's edit
    return (wordcloud, randomNum, image_id)

def dictionary_convert(dict):
    longStr = ""
    for key in dict:
        i = 0
        freq = dict[key]
        while i < freq:
            longStr = longStr + key + " "
            i = i + 1
    
    return longStr

    
def configure_routes():
    # set up a web app with correct routes
    app = Flask(__name__)
    cnx = make_connection()
    db = def_db(cnx)
    fs = GridFS(db)
    @app.route('/', methods=['GET'])
    def home():
        return "scrapper"
    @app.route('/scrape', methods=['GET'])
    def scrapeWeb():
        args = request.args
        word = args.get('word')
        # scrape the web, get the result and store them to db then return success if success
        if not word:
            return "no word"
        result = webscraper.WebScrapeProcedures.procedure_1(word)

        if (len(result) == 0):
            # If there are no results, then the only word that exists is itself.
            result = {word: 10}
        
        # allWords = ",".join(list(result.keys()))

        allWords = dictionary_convert(result)
        # allWords = allWords[0:10000]
        #stores text to db, if it is a new word itll insert the text, if it is a word
        #that is previously in the db itll concatinate the text
        stored_id = store_text(db,word,allWords)
        generate_store_wordcloud(db,fs,word,stored_id)
        
        #return allWords
        #instead of returning the words it will retrieved the id of the stored document
        return allWords
    return app

app = configure_routes()


# turn on debugging if in development mode
if os.getenv('FLASK_ENV', 'development') == 'development':
    # turn on debugging, if in development
    app.debug = True # debug mnode

if __name__ == "__main__":
    app.run(debug=True)