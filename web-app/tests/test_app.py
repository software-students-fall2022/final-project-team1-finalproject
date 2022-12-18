import pytest

import app as App

class TestApp:

    def test_sanity(self):
        assert True, "Sanity check failed."

    def test_def_db(self):
        cxn = App.make_connection()
        assert (cxn is not None)
        db = App.def_db(cxn)
        assert (db != -1)
        print(' *', 'Connected to MongoDB!') # if we get here, the connection worked!
    
    def test_db_exceptions(self):
        cxn = 0
        db = App.def_db(cxn)
        assert (db == -1)

    def test_base_route(self):
        app = App.configure_routes()
        client = app.test_client()
        url = "/"
        response = client.get(url)
        assert response.status_code == 200

    def test_keyword_route(self):
        app = App.configure_routes()
        client = app.test_client()
        url = "/keyword"
        response = client.get(url)
        assert response.status_code == 200

    def test_featured_route(self):
        app = App.configure_routes()
        client = app.test_client()
        url = "/featured"
        response = client.get(url)
        assert response.status_code == 200

    def test_wrong_route(self):
        app = App.configure_routes()
        client = app.test_client()
        url = "/wrong"
        response = client.get(url)
        assert response.status_code == 404

