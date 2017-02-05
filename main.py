from Tables.CategoryTable import CategoryTable
from Tables.ArticleTable import ArticleTable
from Tables.WordTable import WordTable
from WebsiteParsers.WebsiteParser import WebsiteParser


def magyarIdokTest():
    parser = WebsiteParser()
    parser.processRssFeed()


if __name__ == "__main__":
    # parser = WebsiteParser()
    # print(parser.processRssFeed())
    magyarIdokTest()
