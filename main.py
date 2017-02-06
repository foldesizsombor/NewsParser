from Tables.CategoryTable import CategoryTable
from Tables.ArticleTable import ArticleTable
from Tables.WordTable import WordTable
from Tables.SupportedSitesTable import SupportedSitesTable
from Db.Database import Database
from WebsiteParsers.WebsiteParser import WebsiteParser
from WebsiteParsers._444Parser import _444Parser
from WebsiteParsers.HVGParser import HVGParser
from WebsiteParsers.IndexParser import IndexParser
from WebsiteParsers.OrigoParser import OrigoParser
from WebsiteParsers.MagyarIdokParser import MagyarIdokParser
from Models.ArticleModel import ArticleModel


def populateDb():
    parsers = [
        _444Parser(),
        HVGParser(),
        IndexParser(),
        OrigoParser(),
        MagyarIdokParser()
    ]

    for parser in parsers:
        # print(parser.tagParseStyle, parser.tagContainerTag)
        parser.processRssFeed()


def testModels():
    data = ArticleTable().getOne()
    articleModel = ArticleModel(data)
    print(articleModel.getUrl())


if __name__ == "__main__":
    populateDb()
    # testModels()
