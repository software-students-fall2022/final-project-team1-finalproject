
from bs4 import BeautifulSoup
import urllib.request as request

url ="https://en.wikipedia.org/wiki/List_of_terms_relating_to_algorithms_and_data_structures"
headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}

# with urllib.request.urlopen("https://en.wikipedia.org/wiki/List_of_terms_relating_to_algorithms_and_data_structures") as url:
req = request.Request(url, headers=headers)
data = request.urlopen(req).read()

soup= BeautifulSoup(data, "html.parser")
print(soup)
