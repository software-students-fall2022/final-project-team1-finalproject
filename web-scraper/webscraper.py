
from bs4 import BeautifulSoup
from urllib import request
import requests
from googlesearch import search

class WebScrape:
    search_engine = "https://www.google.com/search?q="
    headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}
    parser = "html.parser"

    @staticmethod
    def get_google_search_results(user_input: str):
        '''Given the user input, return a Generator of url string results based on the search'''
        return search(user_input, tld="co.in")

    @staticmethod
    def generate_google_url(user_input: str) -> str:
        '''Given the user input, returns the string for the search query'''
        return WebScrape.search_engine + user_input

    @staticmethod
    def create_request(url: str) -> request:
        '''Given a url, returns a request for the url'''
        return request.Request(url, headers=WebScrape.headers)

    @staticmethod
    def get_data(req: request) -> str:
        '''Given a Request, returns the data fetched from the Request'''
        return request.urlopen(req).read()

    @staticmethod
    def get_requests(url: str):
        '''Uses the requests module to perform a fetch of data based on the url'''
        return requests.get(url)

    @staticmethod
    def parse_data(data: str) -> BeautifulSoup:
        '''Given data, parses the data into a BeautifulSoup object'''
        return BeautifulSoup(data, WebScrape.parser)
    
    @staticmethod
    def clean_dom(dom: BeautifulSoup) -> BeautifulSoup:
        '''Given the dom, remove all the content of the following tags:
        script
        head
        '''
        content = dom.find_all('script, head')
        for e in content:
            e.clear()
        return dom


class WebScrapeProcedures:

    @staticmethod
    def procedure(user_input):
        google_dom = WebScrape.parse_data(WebScrape.get_data(WebScrape.create_request(WebScrape.generate_google_url(user_input))))
        #print(google_dom)
    @staticmethod
    def procedure1(user_input):
        words = {}
        url_generator = WebScrape.get_google_search_results(user_input)
        for url in url_generator:
            req = WebScrape.get_requests(url)
            print("Status: ", req)
            print(req.text[:200])
            dom = WebScrape.parse_data(req.text)
            dom = WebScrape.clean_dom(dom)
            print(dom.find('head'))

            # print(dom[:50])
            input()

            
        
WebScrapeProcedures.procedure1("Hello")

# print(WebScrape.get_google_search_results("HI"))
        
    


# with urllib.request.urlopen("https://en.wikipedia.org/wiki/List_of_terms_relating_to_algorithms_and_data_structures") as url:

