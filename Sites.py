import requests
import bs4 as bs
import re
from multiprocessing import Pool, cpu_count
from Tables import TableModel


class GenericSite:
    parseStyle = {}
    urls = []
    workTitle = ""
    siteId = None  # placeholder variable to store the site id
    blackList = []
    db = None  # placeholder variable to store the db object
    rssTag = None
    articleContainerTag = None

    def __init__(self):
        self.initSite()

    def __del__(self):
        self.destructSite()

    def destructSite(self):
        del self.db

    def initSite(self):
        self.db = TableModel()
        self.blackList = self.db.getBlackList()
        self.urls = self.db.getFeedCategores(self.siteId)

    def getSoupObject(self, url, mode="lxml"):
        res = requests.get(url)
        html = res.content
        soup = bs.BeautifulSoup(html, mode)
        [s.extract() for s in soup('script')]

        return soup

    def processRssFeed(self):
        max_process_count = cpu_count()
        for url in self.urls:
            soup = self.getSoupObject(url)
            links = [[link.text, self.articleContainerTag, self.parseStyle] for link in soup.find_all(self.rssTag)]
            for current_links in range(0, len(links), max_process_count):
                links_to_process = links[current_links:current_links + max_process_count]
                links_to_process = [[parameter[0], parameter[1], parameter[2], i] for i, parameter in
                                    enumerate(links_to_process)]

                article_ids = []
                for link in links_to_process:
                    article_ids.append(self.db.saveArticle(link[0], 0, self.siteId))

                pool = Pool(processes=max_process_count)
                words = pool.map(self.getWordsFromTags, links_to_process)
                pool.close()
                for word in words:
                    # print(word,print(article_ids[word[0]]))
                    self.db.saveWords(word[1:], article_ids[word[0]])

        self.db.commitAllChanges()

    def getWordsFromTags(self, parameter):
        link = parameter[0]
        tag = parameter[1]
        style = parameter[2]
        soupObject = self.getSoupObject(link)
        words = [parameter[3]]
        for i in soupObject.find_all(tag, style):
            myText = i.text
            word = re.findall(r'\w+', myText)
            for x in word:
                d = x.lower()
                if d not in self.blackList:
                    words.append(d.strip())

        return words


class Origo(GenericSite):
    parseStyle = {"id": "article-text"}
    urls = []
    workTitle = "Origo"
    siteId = 0
    rssTag = "guid"
    articleContainerTag = "div"


if __name__ == "__main__":
    site = Origo()
    site.processRssFeed()
