import requests
import bs4 as bs
import re
import pickle
from collections import Counter
from multiprocessing import Pool
class Parser:
    black_list = ["a", "csak", "ezért", "tehát", "ennélfogva", "tudniillik", "amennyiben", "hanem", "pedig", "mégis", "mégse", "nemcsak", "azonban", "ellenben",  "az", "és", "viszont", "hogy", "888", "meg,", "sőt", "sem", "se",  "hu", "http", "de", "egy",]
    # TODO: replace with data source

    def getSoupObject(self, url, mode="lxml"):
        res = requests.get(url)
        html = res.content
        soup = bs.BeautifulSoup(html, mode)

        return soup

    def processRssFeed(self, url, articleTag, tag, style):
        soup = self.getSoupObject(url)
        links = [[link.text, tag, style] for link in soup.find_all(articleTag)]
        pool = Pool(processes=len(links))
        words = pool.map(self.getWordsFromTags,links)
        pool.close()
        return words

    def getWordsFromTags(self, parameter):
        link = parameter[0]
        tag = parameter[1]
        style = parameter[2]
        soupObject = self.getSoupObject(link)
        words = []
        for i in soupObject.find_all(tag, style):
            # TODO: review for loop (join find_all array)
            myText = i.text
            word = re.findall(r'\w+', myText)
            for x in word:
                d = x.lower()
                if d not in self.black_list:
                    words.append(d.strip())
        return words

class Helpers:

    @staticmethod
    def indexCounter( data):
        count = Counter(data)
        return count.most_common(3)

    @staticmethod
    def keyWordCounter(data, keywords):
        counter = {}
        if len(keywords) <= 1:
            counter[keywords[0]] = 0
            for i in data:
                if i in keywords[0]:
                    counter[keywords[0]] += 1
        else:
            for keyword in keywords:
                counter[keyword] = 0
                for i in data:
                    if keyword in i:
                        counter[keyword] += 1
        return counter

if __name__ == "__main__":
    parser = Parser()
    #pickle.dump(,open("articles.pk","wb"))
    print(parser.processRssFeed("http://888.hu/rss/", "guid", "div", {"id": "st"}))
    #words = pickle.load(open("articles.pk","rb"))
    #print(Helpers.keyWordCounter(words,["migráns", "soros"]))

"""
def index_parser():
    black_list = ["a", "az", "és", "viszont", "hogy"]  # TODO: replace with data source

    url = 'http://index.hu/24ora/rss/'
    res = requests.get(url)
    html = res.content
    soup = bs.BeautifulSoup(html, 'lxml')

    for link in soup.find_all('guid'):
        temRes = requests.get(link.text)
        tempHtml = temRes.content
        tempSoup = bs.BeautifulSoup(tempHtml, 'lxml')
        tempWord = []
        for p in tempSoup.find_all('p'):
            # TODO: review for loop (join find_all array)
            myText = p.text
            word = re.findall(r'\w+', myText)
            for x in word:
                d = x.upper()
                if d not in black_list:
                    tempWord.append(d.strip())
        return tempWord


# print(guider())

def nyolcnyolcnyolc():
    nyolcUrl = 'http://888.hu/rss/'
    nyolcRes = requests.get(nyolcUrl)
    nyolcHtml = nyolcRes.content
    nyolcSoup = bs.BeautifulSoup(nyolcHtml, 'lxml')
    nyolcWord = []

    for i in nyolcSoup.find_all('guid'):
        print(i.text)
        word = re.findall(r'\w+', i.text)
        for x in word:
            # print(x)
            d = x.upper()
            if d != "A" and d != "AZ" and d != "ÉS" and d != "DE" and d != "VISZONT" and d != "HOGY" and d != 'HTTP' and d != '888' and d != 'HU':
                nyolcWord.append(d.strip())
    return nyolcWord
    # print(nyolcWord)
"""