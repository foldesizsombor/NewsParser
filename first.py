import requests
import bs4 as bs
import re
from collections import Counter

def guider():

    url = 'http://index.hu/24ora/rss/'
    res = requests.get(url)
    html = res.content
    soup = bs.BeautifulSoup(html, 'lxml')

    for link in soup.find_all('guid'):
        temRes = requests.get(link.text)
        tempHtml = temRes.content
        tempSoup = bs.BeautifulSoup(tempHtml,'lxml')
        tempWord = []
        for p in tempSoup.find_all('p'):
            myText = p.text
            word = re.findall(r'\w+', myText)
            for x in word:
                d = x.upper()
                if d != "A" and  d != "AZ" and d != "ÉS" and d != "DE" and d != "VISZONT" and d != "HOGY":
                    tempWord.append(d.strip())
        return tempWord
#print(guider())
def indexCounter():
    adat = guider()
    count = Counter(adat)
    print(count.most_common(3))
#indexCounter()
def indexTitleTester():
    for link in soup.find_all('guid'):
        linkem = []
        linkem.append(link.text)
        for i in linkem:
            tempUrl = i
            tempREs = requests.get(tempUrl)
            tempHtml = tempREs.content
            tempSoup = bs.BeautifulSoup(tempHtml,'lxml')
            for p in tempSoup.select('title'):
                print(p.text)
#titleTester()

def nyolcnyolcnyolc():
    nyolcUrl = 'http://888.hu/rss/'
    nyolcRes = requests.get(nyolcUrl)
    nyolcHtml = nyolcRes.content
    nyolcSoup = bs.BeautifulSoup(nyolcHtml,'lxml')
    nyolcWord = []

    for i in nyolcSoup.find_all('guid'):
        print(i.text)
        word = re.findall(r'\w+', i.text)
        for x in word:
            #print(x)
            d = x.upper()
            if d != "A" and d != "AZ" and d != "ÉS" and d != "DE" and d != "VISZONT" and d != "HOGY" and d!= 'HTTP' and d != '888' and d != 'HU':
                nyolcWord.append(d.strip())
    return nyolcWord
    #print(nyolcWord)

nyolcnyolcnyolc()
def nyolcTest():
    adat = nyolcnyolcnyolc()
    for i in adat:
        print(i)
#test()

def nyolcTest():
    url = 'http://888.hu/article-ez-a-budapesti-hotel-lett-a-vilag-legjobb-szallodaja'
    nyolcRes = requests.get(url)
    nyolcHtml = nyolcRes.content
    nyolcSoup = bs.BeautifulSoup(nyolcHtml, 'lxml')
    for i in nyolcSoup.find_all('p'):
        print(i.text)
#test()

def negynegynegy():
    pass
