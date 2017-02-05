from Db.Database import Database


class TableModel:
    """
    This class is the common ancestor of the table objects.
    Each table object represents database tables
    """
    tableName = ""  # Stores the name of the table in the database

    def __del__(self):
        # Database.closeDb()
        pass

    def getTableName(self):
        return self.tableName

    def getOne(self, filters=None):
        """
        :param filters:
        :return:
        """
        return self._getTableData(filters, 1)

    def getMany(self, limit, filters=None):
        """
        :param limit:
        :param filters:
        :return:
        """
        return self._getTableData(filters, limit)

    def getAll(self, filters=None):
        """
        :param filters:
        :return:
        """
        return self._getTableData(filters)

    def getCount(self):
        return len(self._getTableData())

    def addDataToTable(self, data, save=True):
        """
        :param data:
        :param save:
        :return:
        """
        self._insertIntoTable(data, save)

    def _getTableData(self, filters=None, limit=None):
        """
        :param      dict|None filters:
        :param      int|None  limit:
        :return     list|None:
        """

        query = ""
        param_values = []

        if filters:
            parameter_names = filters.keys()
            param_values = [filters[i] for i in parameter_names]
            parameters = " = ?  AND ".join(parameter_names) + " = ? "
            query = 'SELECT * FROM ' + self.getTableName() + " WHERE " + parameters

        else:
            param_values = None
            query = 'SELECT * FROM ' + self.tableName
        if limit:
            query += " LIMIT " + str(limit)
        query += ";"
        print(query)
        isSucessfull = Database.execute_query(query, param_values)
        return isSucessfull

    def _insertIntoTable(self, data, save=True):
        """
        :param  dict data:
        :return bool:
        """
        values = []
        keys = []
        for i in data.keys():
            if (type(data[i]) == str):
                data[i] = "'" + data[i] + "'"
            values.append(str(data[i]))
            keys.append(i)
        keys = "(" + ", ".join(keys) + ")"
        query = "INSERT INTO " + self.tableName + keys + " VALUES( " + ", ".join(values) + " );"
        print(query)
        is_sucessfull = Database.execute_query(query)
        if save:
            Database.saveChanges()
        return is_sucessfull
