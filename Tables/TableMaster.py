from Tables.TableModel import TableModel


class TableMaster(TableModel):
    tableName = "sqlite_master"

    def getAllTableName(self):
        tables = self.getAll({"type": "table"})
        return [columns[1] for columns in tables]
