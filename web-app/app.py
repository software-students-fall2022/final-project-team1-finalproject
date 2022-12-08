from flask import Flask, render_template, request, redirect, abort, url_for, make_response, flash,send_file
import os
import requests
from bson.objectid import ObjectId
from gridfs import GridFS
from pymongo import MongoClient
import base64
from io import BytesIO
import certifi
import codecs




client = MongoClient("mongodb+srv://aleolazabal:Aleoli199!@mongodb.unpvyhj.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = client.test
fs = GridFS(db)

def configure_routes():
    # set up a web app with correct routes
    app = Flask(__name__)
    @app.route('/')
    def home():
        return render_template("home.html")

    @app.route('/keyword' , methods=['GET'])
    def generate():
        # args = request.args
        # word = args.get('word')
        # payload = {'word':word}
        # # send request to the web scraper, add the keyword as the query string
        # #message = requests.get('http://scraper:5000/scrape', params=payload)

        company = db.inputs.find_one({"name" : "meta"})#will find the input on the database based on the input
        #right now meta is the example but we should soon be able to take any keyword

        image_id = company["image_id"]
        image = fs.get(ObjectId(image_id)) #gets the image from fs files

        base64_data = codecs.encode(image.read(), 'base64')
        image = base64_data.decode('utf-8') 

        return render_template("home.html", image = image)#pass in the image to be rendered

    return app

app = configure_routes()

if __name__ == "__main__":
    app.run(debug=True)