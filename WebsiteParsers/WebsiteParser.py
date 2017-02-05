import requests
import bs4 as bs
import re
from multiprocessing import Pool, cpu_count

import time

from Tables.BlackListTable import BlackListTable
from Tables.ArticleTable import ArticleTable
from Tables.WordTable import WordTable
from Tables.CategoryTable import CategoryTable
from Tables.SupportedSitesTable import SupportedSitesTable


class WebsiteParser:
    """
    This is the common ancestor of the  parser objects.
    Each WebsiteParser object is able to connect to a website, and parse trough it's rss feed,
        process it using the multiprocessing module, and saving some of their content to the database
        trough the Table objects

    Attributes:
        :var categoryUrls (list)
            Some of the websites has categories to structure their content,
                so a the parser might have to parse trough more than one url.
            The parser uses the urls list to store these urls
        :var parseStyle (dict)
            The parser uses tags, and css styles(eg.:id,class) to parse the content of the site.
            It uses this dictionary to store these parameters
        :var siteId (int)
            Every website is represented by an id in the database. To be able to get website specific data from
                the db, the object has to store it's id.
        :var rssTag ()

    """

    categoryUrls = []
    parseStyle = {}
    siteId = 3
    rssTag = ""
    articleContainerTag = ""
    excludedTags = ["script", "footer"]

    def __init__(self):
        self.initParser()

    def __del__(self):
        self.destructParser()

    def destructParser(self):
        del self.blackListTable
        del self.articleTable
        del self.wordTable
        del self.categoryTable

    def initParser(self):
        self.blackListTable = BlackListTable()
        self.articleTable = ArticleTable()
        self.wordTable = WordTable()
        self.categoryTable = CategoryTable()
        self.sitesTable = SupportedSitesTable()

        categories = self.categoryTable.getAll({"site_id": self.siteId})
        self.categoryIds = [category[0] for category in categories]
        self.categoryUrls = [category[1] for category in categories]

        blackList = self.blackListTable.getAll()
        self.blackList = [blackword[0] for blackword in blackList]

        site = self.sitesTable.getOne({"id": self.siteId})[0]
        if site[2] != "0":
            self.parseStyle["id"] = site[2]
        elif site[3] != "0":
            self.parseStyle["class"] = site[3]

        self.articleContainerTag = site[4]
        self.rssTag = site[5]

    def _getSoupObject(self, url, mode="lxml"):
        """
        makes a beautiful soup object out of a url.
        this method only supposed to use internally
        :param url:
        :param mode:
        :return:
        """
        tags_to_extract = self.excludedTags
        res = requests.get(url)
        html = res.content
        soup = bs.BeautifulSoup(html, mode)
        if tags_to_extract:
            for i in tags_to_extract:
                [s.extract() for s in soup(tags_to_extract)]
        return soup

    def processRssFeed(self):
        """
        Processes the website's rss feed, and saves the words and articles to the database
        """
        max_process_count = cpu_count()
        time_stamp = int(time.time())

        # loops through the category urls
        for i, url in enumerate(self.categoryUrls):
            soup = self._getSoupObject(url)
            # creates a list witch contains lists of a link's url,
            # and the tag and the style of the section we want to get
            links = [[link.text.split("#")[0], self.articleContainerTag, self.parseStyle] for link in
                     soup.find_all(self.rssTag)]
            print(links)
            # loops trough the links. It's using the amount of the cpu cores to decide the step size if the loop.
            # so for example if the computer has 8 cores it steps by 8.
            # this is necessary because the multiprocessing module is only stable if it has less processes than the cpu
            # cores.
            for current_links in range(0, len(links), max_process_count):

                # Selects the links to pass to the multiprocessing function.
                # It's slicing the links list by the amount of the cpu cores.
                links_to_process = links[current_links:current_links + max_process_count]
                # Adds an index to each link to be able to sort them once the multiprocessing functions finished
                links_to_process = [[parameter[0], parameter[1], parameter[2], i] for i, parameter in
                                    enumerate(links_to_process)]

                # Adds an new row to the articles table for each link, and saves it
                article_ids = []
                for link in links_to_process:
                    # Adds a new row to the articleTable
                    self.articleTable.addDataToTable(
                        {"url": link[0],
                         "datetime": time_stamp,
                         "category_id": self.categoryIds[i],
                         "siteId": self.siteId
                         },
                        False)
                    # Fetches the id of the new article
                    article_ids.append(
                        self.articleTable.getOne(
                            {"url": link[0],
                             "datetime": time_stamp,
                             "category_id": self.categoryIds[i]}
                        )[0][0]
                    )

                # Sets the pool size to the amount of the cpu cores
                pool = Pool(processes=max_process_count)
                pool_output = pool.map(self._getWordsFromTags, links_to_process)
                # When the map is done we close the pool
                pool.close()
                # Saves the words to the database
                for words in pool_output:
                    # The first data in the words list is used to detect the word's context(article)
                    for word in words[1:]:
                        # If it's the last word to save it saves the changes to the database
                        if words == pool_output[-1] and word == words[-1]:
                            self.wordTable.addDataToTable(
                                {"text": word, "article_id": article_ids[words[0]]},
                                True)
                        else:
                            self.wordTable.addDataToTable(
                                {"text": word, "article_id": article_ids[words[0]]},
                                False)

    def _getWordsFromTags(self, parameter):
        """
        This method parses trough a page on a website,
        and collects the words inside a specific tag with a specific style.
        It is called by the multiprocessing module, and runs simultaneously on every core of the cpu
        This method should only be used internally
        :param parameter: contains the url of the webpage, and the tag, and style of the parsed element
        :return:          a list of words that contains the words context(articleId) in the first element of the list
        """
        link = parameter[0]
        tag = parameter[1]
        style = parameter[2]
        soupObject = self._getSoupObject(link)
        words = [parameter[3]]
        for i in soupObject.find_all(tag, style):
            myText = i.text
            word = re.findall(r'\w+', myText)
            for x in word:
                d = x.lower()
                if d not in self.blackList:
                    words.append(d.strip())

        return words
