import requests
import bs4 as bs
import re
from collections import Counter
import nltk
from nltk import word_tokenize


url = 'http://index.hu/belfold/2017/01/20/soros_beszolt_az_alcivilezo_kormanynak_az_mti_kihagyta/'
res = requests.get(url)
html = res.content
soup = bs.BeautifulSoup(html,'lxml')

def ablak():
    for i in soup.find_all('p'):
        a = i.text.upper()
        print(a)
        for i in a:
            count = 0
            if "SOROS" in i:
                count +=1
    print(count)

def nltkval():
    for i in soup.find_all('p'):
        a = i.text
        alma = a.split()
        token = word_tokenize(a)
        #print(token)
        words = [w.lower() for w in token]
        print(sorted(set(words)))

#nltkval()
def regexel():
    count = 0

    for i in soup.find_all('p'):
        a = i.text
        asd = a.split
        word = re.findall(r'\w+', a)
        words = [w.lower() for w in word]
        print(words)

        for i in words:
            if "soros" in i:
                count += 1
        #print(sorted(set(words)))
    print(count)
#egexel()

def counter():
    z
    a = Counter(myArray)
    print(a.most_common()[0])
counter()
