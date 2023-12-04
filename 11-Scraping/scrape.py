import requests
from bs4 import BeautifulSoup


response = requests.get(
    url='https://en.wikipedia.org/wiki/Machine_learning'
)

print(response.status_code)

soup = BeautifulSoup(response.content, 'html.parser')
body = soup.find(id='bodyContent')

allLinks = soup.find(id='bodyContent').find_all('a')
onlyLinks = []

for link in allLinks:
    link_str = link.get('href')
    if str(link_str).find('#') == -1:
        onlyLinks.append(link_str)


article_text = soup.get_text()

import nltk
nltk.download('punkt')
import string

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
processed_article = article_text.lower()
processed_article = re.sub(r'\s+', ' ', processed_article)
processed_article = re.sub(r'[!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~]','', processed_article)
# Preparing the dataset
all_sentences = sent_tokenize(processed_article)
# 
all_words = [word_tokenize(sent) for sent in all_sentences]

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
# Removing Stop Words
stops = set(stopwords.words('english'))
for i in range(len(all_words)):
    all_words[i] = [w for w in all_words[i] if w not in stops]