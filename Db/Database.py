import sqlite3


class Database:
    """
    This is the database wrapper class.
    It's using the singleton programing pattern so it doesn't have to make a
    new connection every time a query is executed.

    Attributes:
        connection (Object): Holds the current connection

    """
    connection = None

    @classmethod
    def getConnection(cls, is_new=False):
        """
        :param is_new: if the variable is true the method makes a new connection
        :return:       returns a connection
        """
        if not cls.connection and is_new == False:
            cls.connection = sqlite3.connect("C:/Users/farka/PycharmProjects/Nyugat_website/NewsParser/Db/database.db",
                                             timeout=10)
        return cls.connection

    @classmethod
    def execute_query(cls, query, query_parameters=None):
        """
        :param query:               the query that needs to be executed
        :param query_parameters:    the parameters of the query Eg: SELECT * FROM table_name WHERE id = ?
        :return:                    returns the data provided by the fetchall() method
        """
        connection = cls.getConnection()
        cursor = None
        data = None
        try:
            cursor = connection.cursor()
        except Exception as exception:
            print("WARNING:", exception)

        if cursor:
            if not query_parameters:
                query_parameters = ()
            response = cursor.execute(query, query_parameters)
            try:
                data = response.fetchall()
            except AttributeError:
                data = None
        return data

    @classmethod
    def saveChanges(cls):
        """
        This method is providing an interface to commit the changes to the database
        """
        cls.connection.commit()

    @classmethod
    def closeDb(cls):
        """
        This method is providing an interface to close the connection to the database
        """
        if cls.connection:
            cls.connection.close()
            cls.connection = None


"""
if __name__ == "__main__":
    Database.getConnection()
    print(Database.execute_query('SELECT * FROM category_urls WHERE id = ?', (0,)))
    Database.closeDb()
"""
