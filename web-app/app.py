from flask import Flask, render_template, request, redirect, abort, url_for, make_response, flash

import os

def configure_routes():
    # set up a web app with correct routes
    app = Flask(__name__)
    @app.route('/')
    def home():
        return "test"

    return app

app = configure_routes()

if __name__ == "__main__":
    app.run(debug=True)