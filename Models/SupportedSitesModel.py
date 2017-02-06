from Models.Model import Model
from Tables.SupportedSitesTable import SupportedSitesTable


class SupportedSitesModel(Model):
    _relatedTable = SupportedSitesTable

    def getId(self):
        return self.getField("id")

    def getTitle(self):
        return self.getField("title")

    def getArticleContainerId(self):
        return self.getField("article_container_id")

    def getArticleContainerClass(self):
        return self.getField("article_container_class")

    def getArticleContainerTag(self):
        return self.getField("article_container_tag")

    def getTagContainerTag(self):
        return self.getField("tag_container_tag")

    def getTagContainerClass(self):
        return self.getField("tag_container_class")

    def getTagContanerId(self):
        return self.getField("tag_container_id")
