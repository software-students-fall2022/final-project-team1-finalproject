from flask import Flask, render_template, request, redirect, abort, url_for, make_response, flash

import os

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
    return app

app = configure_routes()

if __name__ == "__main__":
    app.run(debug=True)