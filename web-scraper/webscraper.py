
from bs4 import BeautifulSoup
from urllib import request
import requests
from requests.exceptions import ReadTimeout
# import re
from googlesearch import search

class WebScrape:
    search_engine = "https://www.google.com/search?q="
    headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}
    parser = "html.parser"

    @staticmethod
    def get_google_search_results(user_input: str):
        '''Given the user input, return a Generator of url string results based on the google search'''
        return search(user_input, tld="co.in")

    @staticmethod
    def generate_google_url(user_input: str) -> str:
        '''Given the user input, returns the string for the google search query
        
        @deprecated no longer needed
        '''
        return WebScrape.search_engine + user_input

    @staticmethod
    def create_request(url: str) -> request:
        '''Given a url, returns a request for the url

        @deprecated no longer used
        '''
        return request.Request(url, headers=WebScrape.headers)

    @staticmethod
    def get_data(req: request) -> str:
        '''Given a Request, returns the data fetched from the Request
        
        @deprecated no longer used
        '''
        return request.urlopen(req).read()

    @staticmethod
    def get_requests(url: str):
        '''Uses the requests module to perform a fetch of data based on the url'''
        return requests.get(url, headers=WebScrape.headers, timeout=3)

    @staticmethod
    def make_soup(data: str) -> BeautifulSoup:
        '''Given data, parses the data into a BeautifulSoup object'''
        return BeautifulSoup(data, WebScrape.parser)

class WebScrapeCleaner:

    @staticmethod
    def clean_dom(dom: BeautifulSoup) -> BeautifulSoup:
        '''Given the dom, remove all of the following tags:
        script 
        head
        style
        footer
        '''
        content = dom.find_all(['script', 'head', 'style', 'footer'])
        for e in content:
            e.clear()
        return dom

    # Note: Might want to try making this better using regex
    @staticmethod
    def clean_string(string: str) -> str:
        '''Cleans up the string by separating the words based on capitalization.
        '''

        s = " "
        for c in string:
            if c.isupper() and not s[-1].isupper():
                s += ' '
            s += c
        # " ".join([s for s in re.split("([A-Z][^A-Z]*)", string) if s])
        return s

    # TODO: Might want to add the stop words into this method to remove them.
    @staticmethod
    def include_word(word: str) -> bool:
        '''Determines whether the word should be included in the frequency list.
        True for yes, False for no.
        '''
        if len(word) > 30:
            return False
        elif len(word) < 4:
            return False
        elif not word.isalnum():
            return False
        return True

    @staticmethod
    def refactor_weird_words(words: list[str]) -> list[str]:
        '''Given an array of words, returns a new array of only words that are valid
        '''
        refactored = []
        for word in words:
            if WebScrapeCleaner.include_word(word):
                refactored.append(word)
        return refactored


class WebScrapeHelper:

    @staticmethod
    def stop_condition(words: dict) -> bool:
        '''If the number of distinct words and the frequency of the most common word 
        is above a certain threshold, returns True. Otherwise, false is returned.
        '''
        if len(words.keys()) > 30 and max(words.values()) > 200:
            return True
        return False
    
    @staticmethod
    def generate_word_freq_dict(words: list[str]) -> dict[str, int]:
        '''Given a list of strings, create a word freq dictionary'''
        word_freq = {}
        for word in words:
            if word_freq.get(word, None) == None:
                word_freq[word] = 1
            else:
                word_freq[word] += 1
        return word_freq

    @staticmethod
    def make_word_freq_dict(data: str) -> dict[str, int]:
        '''Given the result of the requested url as a string, returns a word freq 
        dictionary after parsing out the unnecessary words.
        '''

        # convert the html string into a soup
        # print("Making soup")
        dom = WebScrape.make_soup(data)

        # clean up the dom by removing unnecessary text inside specific tags
        # print("Cleaning dom")
        dom = WebScrapeCleaner.clean_dom(dom)

        # clean up the string of the remaining text of the beautiful soup
        # print("Cleaning string")
        word_string = WebScrapeCleaner.clean_string(dom.text)

        # split by whitespace
        # print("Spliting by whitespace")
        words = word_string.split()

        # refactor any words that are not good (i.e., likely to be an invalid word)
        # print("Refactoring words")
        words = WebScrapeCleaner.refactor_weird_words(words)

        # Generate the word freq dictionary and return it
        # print("Generating word freq dict for", len(words), "words")
        return WebScrapeHelper.generate_word_freq_dict(words)
    
    @staticmethod
    def combine_word_freq_dicts(dict1: dict[str, int], dict2: dict[str, int]) -> dict[str, int]:
        '''Adds all words of dict2 into dict1 and returns dict1.
        '''
        for word in dict2.keys():
            if dict1.get(word, None) == None:
                dict1[word] = 1
            else:
                dict1[word] += dict2[word]
        return dict1

class WebScrapeProcedures:

    @staticmethod
    def procedure_1(user_input):
        word_freq = {}
        url_generator = WebScrape.get_google_search_results(user_input)
        for url in url_generator:
            print("Current url: ", url)
            try:
                req = WebScrape.get_requests(url)
            except ReadTimeout as t:
                print("Timed out:", t)
                continue
            print("Status: ", req.status_code)
            if (req.status_code != 200):
                print("Error in request. Status code:", req.status_code)
                continue
            else:
                new_word_freq = WebScrapeHelper.make_word_freq_dict(req.text)
                WebScrapeHelper.combine_word_freq_dicts(word_freq, new_word_freq)
                if (WebScrapeHelper.stop_condition(word_freq)):
                    break

        print("Number of unique words:", len(word_freq.keys()))
        print("Some examples:", list(word_freq.keys())[:10])
        print("Highest freq word:", max(word_freq.keys(), key=lambda k: word_freq[k]), max(word_freq.values()))
        print("Longest word length:", max(word_freq.keys(), key=lambda k: len(k)))
        return word_freq

# WebScrapeProcedures.procedure_1("facebook")
