from flask import Flask, render_template
import pytest
import pymongo
import mongomock
import os

from app import make_connection
from app import def_db
from app import configure_routes

class TestApp:

    def test_sanity(self):
        assert True, "Sanity check failed."
    
    def test_def_db(self):
        cxn = make_connection()
        assert (cxn is not None)
        db = def_db(cxn)
        assert (db != -1)
        print(' *', 'Connected to MongoDB!') # if we get here, the connection worked!
    
    def test_base_route(self):
        app = configure_routes()
        client = app.test_client()
        url = '/'
        response = client.get(url)
        assert response.status_code == 200
    
    def test_wrong_route(self):
        app = configure_routes()
        client = app.test_client()
        url = '/test'
        response = client.get(url)
        assert response.status_code == 404