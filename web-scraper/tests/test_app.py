import pytest
import mongomock
from gridfs import GridFS
from wordcloud import WordCloud, STOPWORDS
import math
import random

import app as AlejandroApp

class TestAlejandroApp:

    def test_sanity(self):
        assert True, "Sanity check failed."

    @pytest.mark.parametrize("word, text", [
        ("meta", "meta zuckerberg harvard platforms"),
        ("amazon", "bezos employee cloud whole foods"),
        ("fifa", "messi soccer ronaldo world cup"),
        ("meta", "zuckerberg harvard meta platforms"),
        ("amazon", "cloud bezos employee whole foods"),
        ("fifa", "world cup messi soccer ronaldo")
    ]) 

    def test_store_text(self , word, text): 

        # create a database using mongomock
        db = mongomock.MongoClient().db.collection

        # create an empty inputs collection or fetch the inputs collection
        inputs = db["inputs"]

        # check if the inputs collection already has the word from a previous search
        # return the document with the word 
        found = inputs.find_one({"word":word})

        # call store_text()
        AlejandroApp.store_text(db, word, text)
        numRounds = inputs.count_documents({})
        rndTracker = 1

        # check if the last document is the inserted document
        for rnd in inputs.find():
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
        # create a database using mongomock
        db = mongomock.MongoClient().db.collection

        # store word and text in the database before generating the wordcloud
        id = AlejandroApp.store_text(db, word, text)

        # run generate_store_wordcloud on the id and parameters
        retTuple = AlejandroApp.generate_store_wordcloud(db, word, id)
        retWordcloud = retTuple[0]
        retRandomState = retTuple[1]
        retImageId = retTuple[2]

        # inputs and history collections
        inputs = db["inputs"]
        histories = db["history"]

        # compare imageIds
        input = inputs.find_one({"_id" : id})
        assert input["image_id"] == retImageId

        history = histories.find_one({"image_id" : retImageId})
        assert history["word"] == word

        # generate a test wordcloud
        wordcloud = WordCloud(stopwords=STOPWORDS, background_color="white", max_words=100, random_state=retRandomState,collocations=False,width=1280, height=720).generate(text)

        # compare wordclouds
        assert wordcloud.words_ == retWordcloud.words_
        


        
        

        

