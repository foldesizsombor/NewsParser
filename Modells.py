import sqlite3


class Modell:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()

    def getBlackList(self):
        black_list = [i for i in self.c.execute('SELECT * FROM black_list')]
        return black_list
