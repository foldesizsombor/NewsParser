from Models.Model import Model
from Tables.CategoryTable import CategoryTable


class CategoryModel(Model):
    _relatedTable = CategoryTable

    def getId(self):
        return self.getField("id")

    def getUrl(self):
        return self.getField("url")

    def getSiteId(self):
        return self.getField("site_id")
