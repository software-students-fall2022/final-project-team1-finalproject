import pytest
from webscraper import WebScrape as WS
from webscraper import WebScrapeCleaner as WSC
from webscraper import WebScrapeHelper as WSH
from webscraper import WebScrapeProcedures as WSP
import types
from urllib import request
import requests
from bs4 import BeautifulSoup
import mongomock

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
        assert str(expected) == actual, "Expected the data fetched to be the same"

    def test_get_requests(self):
        expected = open('./tests/data/example.txt', 'r').read()
        actual = WS.get_requests("https://example.com")
        assert actual.status_code == 200, "Expected status code to be 200"
        assert expected == actual.text, "Expected the content to be the same"

    def test_make_soup(self):
        html = open('./tests/data/example.txt', 'r').read()
        soup = WS.make_soup(html)
        assert isinstance(soup, BeautifulSoup), "Expected a beautifulsoup to be created"

class TestWebScrapeCleaner:
    def test_clean_soup(self):
        html = open('./tests/data/example.txt', 'r').read()
        soup = BeautifulSoup(html, WS.parser)
        soup = WSC.clean_soup(soup)

        expected_empty_text = soup.find_all(['script', 'head', 'style', 'footer'])
        for element in expected_empty_text:
            assert element.text == "", "Expected the text for the " + element.name +" element to be removed"
    
    def test_clean_string(self):
        string = "Hello WorldThis is the TextThat will be tested DDL inclusionDLL."
        actual = WSC.clean_string(string)
        expected = "Hello World This is the Text That will be tested DDL inclusion DLL."
        assert expected == actual, "Expected the cleaning of the string to work correctly"
        
    def test_clean_string_1(self):
        string = ""
        actual = WSC.clean_string(string)
        expected = ""
        assert expected == actual, "Expected the cleaning of the string to work correctly"

    def test_clean_string_2(self):
        string = "Hello World."
        actual = WSC.clean_string(string)
        expected = "Hello World."
        assert expected == actual, "Expected the cleaning of the string to work correctly"

    def test_include_word(self):
        false_words = ['thiS', 'thIs', 'this', 'is', 'the', 'testing.']
        true_words = ['hello', 'world', 'CS101', '1232232202', 'interesting', 'fun', 'byte', 'wIll']
        for word in false_words:
            assert not WSC.include_word(word), "Expected false to be returned for the word"
        for word in true_words:
            assert WSC.include_word(word), "Expected true to be returned for word"
    
    def test_refactor_words(self):
        to_refactor = ['Today', 'is', 'a', 'great', 'day', 'to', 'go', 'outside', 'for', 'hours', 'and', 'have', 'fun.', 'I', 'am', 'taking', 'CS101', 'next', 'semester']
        expected = ['Today', 'Great', 'Day', 'Outside', 'Hours', 'Fun', 'Taking', 'Cs101', 'Next', 'Semester']
        assert WSC.refactor_words(to_refactor) == expected, "Expected only valid words to be stored"

class TestWebScrapeHelper:
    def test_stop_condition(self):
        false_stops = [{}, {'hello': 300, 'bye': 20, 'hello': 20}, {'hello': 200}]
        for d in false_stops:
            assert not WSH.stop_condition(d), "Expected stop condition to not be reached"
        
        true_stops = [{str(k): int(v) for k, v in enumerate(range(2001))}]
        for d in true_stops:
            assert WSH.stop_condition(d), "Expected stop condition to be reached"
        
    def test_generate_word_freq_dict(self):
        words = ['hello', 'hello', 'today', 'is', 'a', 'great', 'day', 'outside']
        expected = {'today': 1, 'hello': 2, 'is': 1, 'a':1, 'great': 1, 'day': 1, 'outside': 1}
        assert WSH.generate_word_freq_dict(words) == expected, "Expected dictionaries generated to have same key value pairs"

    def test_make_word_freq_dict(self):
        sentences = "Hello This is the best day to do some coding. It is also a great day outside"
        expected = {'Hello': 1, 'Best': 1, 'Day': 2, 'Coding': 1, 'Great': 1, 'Outside': 1}
        actual = WSH.make_word_freq_dict(sentences)
        assert actual == expected, "Expected dictionaries generated to have same key value pairs"

    def test_combine_word_freq_dicts(self):
        expected = {'Hello': 1, 'Best': 1, 'Day': 2, 'Coding': 1, 'Great': 1, 'Outside': 1}
        actual = WSH.combine_word_freq_dicts({'Hello': 1, 'Best': 1, 'Day': 1, 'Coding': 1}, {'Great': 1, 'Day': 1, 'Outside': 1})
        assert actual == expected, "Expected dictionaries to be successfully combined"

    def test_fetch_data(self):
        url_200 = "https://example.com"
        res = WSH.fetch_data(url_200)
        expected = open('./tests/data/example.txt', 'r').read()
        assert res.status_code == 200, "Expected successful fetch of the url"
        assert res.text == expected, "Expected the text result to be the same"
    
    def test_fetch_data_timeout(self):
        url = "http://www.google.com:81/"
        res = WSH.fetch_data(url)
        assert res == None, "Nothing should be returned for a timeout url"

    def test_fetch_data_invalid(self):
        url = "invalidurl"
        res = WSH.fetch_data(url)
        assert res == None, "Nothing should be returned for an invalid url"

    def test_print_word_freq_dict_details(self):
        # No exceptions should be thrown 
        WSH.print_word_freq_dict_details({})
        WSH.print_word_freq_dict_details({'Hello': 1, 'Best': 1, 'Day': 2, 'Coding': 1, 'Great': 1, 'Outside': 1})

class TestWebScrapeProcedures:

    def test_procedure_1(self):
        user_input = "hello"
        actual = WSP.procedure_1(user_input)
        assert isinstance(actual, dict), "Expected dictionary to be returned"
    
    def test_procedure_2(self):
        user_input = "hello"
        actual = WSP.procedure_2(user_input)
        assert isinstance(actual, dict), "Expected dictioanry to be returned"

    def test_procedure_1_no_results(self):
        user_input = "1234567898765678264923874"
        assert WSP.procedure_1(user_input) == {}, "Expected no results to appear"

    def test_procedure_2_no_results(self):
        user_input = "1234567898765678264923874"
        assert WSP.procedure_2(user_input) == {}, "Expected no results to appear"
