from Models.Model import Model
from Tables.BlackListTable import BlackListTable


class BlackListModel(Model):
    _relatedTable = BlackListTable

    def getBlackList(self):
        return self.getField("keys")
