from Models.Model import Model
from Tables.WordTable import WordTable


class WordModel(Model):
    _relatedTable = WordTable

    def getId(self):
        return self.getField("id")

    def getArticleId(self):
        return self.getField("article_id")

    def getText(self):
        return self.getField("text")
