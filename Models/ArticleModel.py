from Models.Model import Model
from Tables.ArticleTable import ArticleTable


class ArticleModel(Model):
    _relatedTable = ArticleTable

    def getId(self):
        return self.getField("id")

    def getSiteId(self):
        return self.getField("siteId")

    def getDateTime(self):
        return self.getField("datetime")

    def getCategoryId(self):
        return self.getField("category_id")

    def getUrl(self):
        return self.getField("url")
