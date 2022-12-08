from flask import Flask, render_template, request, redirect, abort, url_for, make_response, flash
from wordcloud import WordCloud
from bs4 import BeautifulSoup
from gridfs import GridFS
from pymongo import MongoClient
from bson.objectid import ObjectId
import certifi
import os
from io import BytesIO
import requests
from PIL import Image
from numpy import asarray


client = MongoClient("mongodb+srv://aleolazabal:Aleoli199!@mongodb.unpvyhj.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = client.test
fs = GridFS(db)

def configure_routes():
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
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        wordcloud = WordCloud().generate(text)
        image_stream = BytesIO()
        wordcloud.to_image().save(image_stream, format="PNG")
        image_stream.seek(0)
        image_data = image_stream.getvalue()
        image_id = fs.put(image_data)
        db.inputs.insert_one({"name": "meta", "text" : text, "image_id" :ObjectId(image_id)})
        return "success"
    return app

app = configure_routes()

if __name__ == "__main__":
    app.run(debug=True)