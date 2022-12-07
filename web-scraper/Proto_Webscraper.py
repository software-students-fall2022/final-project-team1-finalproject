from bs4 import BeautifulSoup
import urllib.request as request

# word cloud edits
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# url ="https://en.wikipedia.org/wiki/Meta_Platforms"
url ="https://about.meta.com/immersive-learning/?gclid=Cj0KCQiAkMGcBhCSARIsAIW6d0Bwo6nHR51X1TUCmOdbcBJmundYRGqOxuxNZcTkw2X1-6h5l-1ZZj0aAtRuEALw_wcB&gclsrc=aw.ds"
headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}

# with urllib.request.urlopen("https://en.wikipedia.org/wiki/List_of_terms_relating_to_algorithms_and_data_structures") as url:
req = request.Request(url, headers=headers)
data = request.urlopen(req).read()

soup= BeautifulSoup(data, "html.parser")
# main_content= soup.find("div", attrs= {"id" : "mw-content-text"})
main_content= soup.find("div")
lists = main_content.find_all("p")
str = ""
for list in lists:
    info= list.text
    str+=info
    str+=" "
print(str)

# word cloud edits
mask = np.array(Image.open("Desktop/big.png"))
color= ImageColorGenerator(mask)

wordcloud = WordCloud(width=2200, height=2000,
    max_words=400,mask=mask, stopwords=STOPWORDS, background_color="white",
    random_state=42).generate(str)

plt.imshow(wordcloud.recolor(color_func=color),interpolation="bilinear")
plt.axis("off")
plt.show()