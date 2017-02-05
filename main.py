from Tables.CategoryTable import CategoryTable
from Tables.ArticleTable import ArticleTable
from Tables.WordTable import WordTable
from Tables.SupportedSitesTable import SupportedSitesTable

from WebsiteParsers.WebsiteParser import WebsiteParser
from WebsiteParsers._444Parser import _444Parser
from WebsiteParsers.HVGParser import HVGParser
from WebsiteParsers.IndexParser import IndexParser
from WebsiteParsers.OrigoParser import OrigoParser
from WebsiteParsers.MagyarIdokParser import MagyarIdokParser


def test():
    parser = MagyarIdokParser()
    parser.processRssFeed()

if __name__ == "__main__":
    test()
