from Tables.CategoryTable import CategoryTable
from Tables.ArticleTable import ArticleTable
from WebsiteParsers.WebsiteParser import WebsiteParser

if __name__ == "__main__":
    parser = WebsiteParser()
    print(parser.processRssFeed())
