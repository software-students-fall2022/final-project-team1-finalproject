
from bs4 import BeautifulSoup
from urllib import request
import requests
from requests.exceptions import ReadTimeout
from wordcloud import WordCloud, STOPWORDS
import re
import numpy as np
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
        return request.urlopen(req).read().decode()

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
    def clean_soup(soup: BeautifulSoup) -> BeautifulSoup:
        '''Given the soup, remove all of the following tags:
        script 
        head
        style
        footer
        '''
        content = soup.find_all(['script', 'head', 'style', 'footer'])
        for e in content:
            e.clear()
        return soup

    # Note: Might want to try making this better using regex
    @staticmethod
    def clean_string(string: str) -> str:
        '''Cleans up the string by separating the words based on capitalization.
        '''
        return re.sub(r"\s+", r" ", re.sub(r"([A-Z]+)", r" \1", string)).strip()

    @staticmethod
    def include_word(word: str) -> bool:
        '''Determines whether the word should be included as a result.
        True for yes, False for no.
        '''
        if len(word) > 30:
            return False
        elif len(word) < 3:
            return False
        elif not word.isalnum():
            return False
        elif word.lower() in STOPWORDS:
            return False
        return True

    @staticmethod
    def refactor_words(words: list[str]) -> list[str]:
        '''Given an array of words, returns a new array of only words that are valid
        '''
        refactored = []
        for word in words:
            word = re.sub(r'[^\w\s0-9]', '', word)
            if WebScrapeCleaner.include_word(word.lower()):
                refactored.append(word.title())
        return refactored


class WebScrapeHelper:

    @staticmethod
    def stop_condition(words: dict) -> bool:
        '''If the number of distinct words and the frequency of the most common word 
        is above a certain threshold, returns True. Otherwise, false is returned.
        '''
        if len(words.keys()) > 2000 and max(words.values()) > 200:
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
        soup = WebScrape.make_soup(data)

        # clean up the soup by removing unnecessary text inside specific tags
        # print("Cleaning soup")
        soup = WebScrapeCleaner.clean_soup(soup)

        # clean up the string of the remaining text of the beautiful soup
        # print("Cleaning string")
        word_string = WebScrapeCleaner.clean_string(soup.text)

        # split by whitespace
        # print("Spliting by whitespace")
        words = word_string.split()

        # refactor the words that are not good (e.g., likely to be an invalid word, weird capitalizations, etc.)
        # print("Refactoring words")
        words = WebScrapeCleaner.refactor_words(words)

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
    
    @staticmethod
    def fetch_data(url: str):
        '''Given the url, performs a fetch of the data. Prints statements if errors appear.
        '''
        try:
            req = WebScrape.get_requests(url)
            print("Status: ", req.status_code)
            return req
        except ReadTimeout as t:
            print("Timed out:", t)
            return None
        except Exception as e:
            print("Unknown exception:", e)
            return None
    
    @staticmethod
    def print_word_freq_dict_details(word_freq: dict[str, int]) -> None:
        '''Given the word frequency dictionary, makes a printout of the details of the dictionary.
        '''
        print("Number of unique words:", len(word_freq.keys()))
        print("Some examples:", list(word_freq.keys())[:10])
        if len(word_freq.keys()) > 0:
            print("Highest freq word:", max(word_freq.keys(), key=lambda k: word_freq[k]), max(word_freq.values()))
            print("Longest word length:", max(word_freq.keys(), key=lambda k: len(k)))
        else:
            print("Word Freq dictionary:", word_freq)

class WebScrapeProcedures:

    @staticmethod
    def procedure_1(user_input: str) -> dict[str, int]:
        '''This procedure performs web scrapingbased on a user_input, generally expecting
        the same results to be returned for each run.

        A dictionary with the word as the keys and frequency as the values is returned.
        '''

        word_freq = {}
        url_generator = WebScrape.get_google_search_results(user_input)
        for url in url_generator:
            print()
            print("Current url: ", url)
            req = WebScrapeHelper.fetch_data(url)
            if (req == None):
                continue
            elif (req.status_code != 200):
                print("Error in request. Status code:", req.status_code)
                continue
            else:
                try:
                    new_word_freq = WebScrapeHelper.make_word_freq_dict(req.text)
                except Exception as e:
                    print("Failed to create frequency dictionary")
                    continue
                WebScrapeHelper.combine_word_freq_dicts(word_freq, new_word_freq)
                if (WebScrapeHelper.stop_condition(word_freq)):
                    break
        
        WebScrapeHelper.print_word_freq_dict_details(word_freq)
        return word_freq
    
    @staticmethod
    def procedure_2(user_input: str) -> dict[str, int]:
        '''This procedure performs web scraping, but potential variations on the resulting dictionary returned.
        
        A dictionary with the word as the keys and frequency as the values is returned.
        '''

        word_freq = {}
        url_generator = WebScrape.get_google_search_results(user_input)
        for url in url_generator:
            print()
            print("Current url: ", url)
            if (np.random.randint(0, 100) <= 30):
                print("Skipping due to probability")
                continue
            
            req = WebScrapeHelper.fetch_data(url)
            
            if (req == None):
                continue
            elif (req.status_code != 200):
                print("Skipped due to status code")
                continue
            else:
                new_word_freq = WebScrapeHelper.make_word_freq_dict(req.text)
                WebScrapeHelper.combine_word_freq_dicts(word_freq, new_word_freq)
                if (WebScrapeHelper.stop_condition(word_freq)):
                    break
        WebScrapeHelper.print_word_freq_dict_details(word_freq)
        return word_freq
