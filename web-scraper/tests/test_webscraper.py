import pytest
from webscraper import WebScrape as WS
from webscraper import WebScrapeCleaner as WSC
from webscraper import WebScrapeHelper as WSH
from webscraper import WebScrapeProcedures as WSP
import types
from urllib import request
import requests
from bs4 import BeautifulSoup

class TestWebScraper:

    def test_sanity(self):
        assert True, "Sanity check failed."

    def test_get_google_search_results(self):

        actual = WS.get_google_search_results("Hello")
        
        assert isinstance(actual, types.GeneratorType), "Expected a generator to be returned"

        url = next(actual)
        assert isinstance(url, str), "Expected the generator to return strings"

        assert url.startswith('http'), "Expected the url to start with http"
    
    def test_generate_google_url(self):
        expected = "https://www.google.com/search?q=Hello"
        actual = WS.generate_google_url("Hello")
        assert expected == actual, "Expected the google url to be correctly created"

    def test_create_request(self):
        actual = WS.create_request("https://www.google.com/search?q=Hello")
        assert isinstance(actual, request.Request), "Expected a request to be created"
    
    def test_get_data(self):
        req = request.Request("https://example.com", headers=WS.headers)
        expected = open('./tests/data/example.txt', 'r').read()
        actual = WS.get_data(req)
        assert len(expected) == len(actual), "Expected the length of the data fetched to be the same"
        assert str(expected) == actual.decode(), "Expected the data fetched to be the same"

    def test_get_requests(self):
        expected = open('./tests/data/example.txt', 'r').read()
        actual = WS.get_requests("https://example.com")
        assert actual.status_code == 200, "Expected status code to be 200"
        assert expected == actual.text, "Expected the content to be the same"

    def test_make_soup(self):
        html = open('./tests/data/example.txt', 'r').read()
        soup = WS.make_soup(html)
        assert isinstance(soup, BeautifulSoup), "Expected a beautifulsoup to be returned"
        