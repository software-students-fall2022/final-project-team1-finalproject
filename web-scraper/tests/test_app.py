import pytest
import os
import mongomock
import pymongo
from gridfs import GridFS
from wordcloud import WordCloud, STOPWORDS
from flask import Flask, render_template
import math
import random


import app as AlejandroApp

class TestAlejandroApp:

    def test_sanity(self):
        assert True, "Sanity check failed."

    #checks that a valid connection is made
 
    def test_def_db(self):
        cxn = AlejandroApp.make_connection()
        assert (cxn is not None)
        db = AlejandroApp.def_db(cxn)
        assert (db != -1)
        print(' *', 'Connected to MongoDB!') # if we get here, the connection worked!

    def test_dictionary_convert(self):
        input = {"hello":1, "this":2, "is":3,"a":1, "test":4}
        res = AlejandroApp.dictionary_convert(input)
        expected = "hello this this is is is a test test test test "
        assert type(res) is str
        assert (expected == res)
        
    def test_base_route(self):
        app = AlejandroApp.configure_routes()
        client = app.test_client()
        url = "/"
        response = client.get(url)
        assert response.status_code == 200

    def test_scrape_route(self):
        app = AlejandroApp.configure_routes()
        client = app.test_client()
        url = "/scrape?"
        response = client.get(url)
        assert response.status_code == 200

    def test_wrong_route(self):
        app = AlejandroApp.configure_routes()
        client = app.test_client()
        url = "/wrong"
        response = client.get(url)
        assert response.status_code == 404

    @pytest.mark.parametrize("word, text", [
        ("meta", "meta zuckerberg harvard platforms"),
        ("amazon", "bezos employee cloud whole foods"),
        ("fifa", "messi soccer ronaldo world cup"),
        ("meta", "zuckerberg harvard meta platforms"),
        ("amazon", "cloud bezos employee whole foods"),
        ("fifa", "world cup messi soccer ronaldo")
    ]) 

    def test_store_text(self, word, text): 

        cxn = AlejandroApp.make_connection()
        db = AlejandroApp.def_db(cxn)

        # check if the inputs collection already has the word from a previous search
        # return the document with the word 
        found = db.inputs.find_one({"word":word})

        # call store_text()
        AlejandroApp.store_text(db,word, text)
        numRounds = db.inputs.count_documents({})
        rndTracker = 1

        # check if the last document is the inserted document
        for rnd in db.inputs.find():
            if rndTracker == numRounds:
                assert rnd["word"] == word
                assert rnd["text"] == text

    @pytest.mark.parametrize("word, text", [
        ("meta", "meta zuckerberg harvard platforms"),
        ("amazon", "bezos employee cloud whole foods"),
        ("fifa", "messi soccer ronaldo world cup"),
        ("meta", "zuckerberg harvard meta platforms"),
        ("amazon", "cloud bezos employee whole foods"),
        ("fifa", "world cup messi soccer ronaldo")
    ])

    def test_generate_store_wordcloud(self, word, text):

        cxn = AlejandroApp.make_connection()
        db = AlejandroApp.def_db(cxn)
        fs = GridFS(db)

        # store word and text in the database before generating the wordcloud
        id = AlejandroApp.store_text(db, word, text)

        # run generate_store_wordcloud on the id and parameters
        retTuple = AlejandroApp.generate_store_wordcloud(db,fs,word,id)
        retWordcloud = retTuple[0]
        retRandomState = retTuple[1]
        retImageId = retTuple[2]

        # compare imageIds
        input = db.inputs.find_one({"_id" : id})
        assert input["image_id"] == retImageId

        history = db.history.find_one({"image_id" : retImageId})
        assert history["word"] == word

        # generate a test wordcloud
        wordcloud = WordCloud(stopwords=STOPWORDS, background_color="white", max_words=100, random_state=retRandomState,collocations=False,width=1280, height=720).generate(text)

        # compare wordclouds
        assert wordcloud.words_ == retWordcloud.words_
        


        
        

        

