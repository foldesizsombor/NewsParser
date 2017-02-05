import requests
import bs4 as bs
import re
from multiprocessing import Pool, cpu_count
import feedparser
from time import mktime
from datetime import datetime
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

    feedUrls = []
    parseStyle = {}
    siteId = None
    rssTag = ""
    articleContainerTag = ""
    excludedTags = ["script", "footer"]

    def __init__(self):
        self.clearClassVariables()
        self.initParser()

    def __del__(self):
        self.destructParser()

    def clearClassVariables(self):
        """
        Temporary solution, the child objects of the parser tend to inherit these variable's states idk why...
        :return:
        """
        self.feedUrls = []
        self.parseStyle = {}
        self.rssTag = ""
        self.articleContainerTag = ""

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
        self.feedUrls = [category[1] for category in categories]

        blackList = self.blackListTable.getAll()
        self.blackList = [blackword[0] for blackword in blackList]

        site = self.sitesTable.getOne({"id": self.siteId})[0]

        if site[2] != "0":
            self.parseStyle["id"] = site[2]
        elif site[3] != "0":
            self.parseStyle["class"] = site[3]
        # if self.siteId != 4 and self.siteId != 2:


        self.siteName = site[1]
        self.articleContainerTag = site[4]

    def getSoupObject(self, url, mode="lxml"):
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
        for i, url in enumerate(self.feedUrls):
            feed = feedparser.parse(url)
            # creates a list witch contains lists of a link's url,
            # and the tag and the style of the section we want to get
            urls = []
            for link in feed["entries"]:
                # we are using the article's datetime to determinate if it has been already saved
                # sometimes the rss's date has not been formatted properly, if this is the case we attempt to correct it
                # (for an example of this see the rss of origo.hu)
                if not link["published_parsed"]:
                    if "." in link["published"]:
                        link["published"] = link["published"].split(".")[0]
                    link["published_parsed"] = feedparser._parse_date(link["published"] + " +0100")
                if not self.articleTable.getOne({"datetime": mktime(link["published_parsed"])}):
                    meta = [link["link"], self.articleContainerTag, self.parseStyle, mktime(link["published_parsed"])]
                    urls.append(meta)
            if urls:
                self.processUrls(urls, i)

    def processUrls(self, urls, categoryIndex):
        """
        Processes a list of urls useing the multiprocessing module, and saves the words and articles to the database
        """
        max_process_count = cpu_count()
        # loops through the category urls

        # loops trough the urls. It's using the amount of the cpu cores to decide the step size,
        # so for example if the computer has 8 cores it steps by 8.
        # this is necessary because the multiprocessing module is only stable if it has less processes than the cpu
        # cores.
        for current_links in range(0, len(urls), max_process_count):

            # Selects the links to pass to the multiprocessing function.
            # It's slicing the links list by the amount of the cpu cores.
            links_to_process = urls[current_links:current_links + max_process_count]
            # Adds an index to each link to be able to sort them once the multiprocessing functions finished
            links_to_process = [[parameter[0], parameter[1], parameter[2], i, parameter[3]] for i, parameter in
                                enumerate(links_to_process)]

            # Adds an new row to the articles table for each link, and saves it
            article_ids = []
            for link in links_to_process:
                # Adds a new row to the articleTable

                self.articleTable.addDataToTable(
                    {"url": link[0],
                     "datetime": link[4],
                     "category_id": self.categoryIds[categoryIndex],
                     "siteId": self.siteId
                     },
                    False)
                # Fetches the id of the new article
                article_ids.append(
                    self.articleTable.getOne(
                        {"url": link[0],
                         "datetime": link[4],
                         "category_id": self.categoryIds[categoryIndex]}
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
                print(len(words), self.siteName)
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
        This method should only be used internally.
        Due to the limitations of the multiprocessing library the function parameters has been provided by a list

        :param list parameter: contains the url of the webpage, and the tag, and style of the parsed element

        :return list:  A list of words that contains the words context(articleId) in the first element of the list
        """
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
