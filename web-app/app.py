from flask import Flask, render_template, request, redirect, abort, url_for, make_response, flash
import os
import requests
import pymongo

load_dotenv()  # take environment variables from .env.

# turn on debugging if in development mode
if os.getenv('FLASK_ENV', 'development') == 'development':
    # turn on debugging, if in development
    app.debug = True # debug mnode

def configure_routes():
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
        message = requests.get('http://scraper:5000/scrape', params=payload)
        return message.text

    return app

app = configure_routes()

if __name__ == "__main__":
    app.run(debug=True)