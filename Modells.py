import sqlite3
import time


# TODO: make an initDatabase
class Model:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def getBlackList(self):
        black_list = self.c.execute('SELECT * FROM black_list').fetchall()
        return [blacklist[0] for blacklist in black_list]

    def getFeedCategores(self, siteId):
        if type(siteId) != type(None) and type(siteId) == int:
            urls = self.c.execute('SELECT url FROM category_urls WHERE site_id = ?', (siteId,)).fetchall()
            return [url[0] for url in urls]

    def saveArticle(self, url, siteId, categoryId):
        articleId = self.c.execute('SELECT id FROM articles WHERE url = ?', (url,)).fetchone()
        if not articleId:
            max_id = self.c.execute('SELECT max(id) FROM articles').fetchone()[0]
            if max_id:
                max_id += 1
            else:
                max_id = 1
            time_stamp = int(time.time())
            self.c.execute('INSERT INTO articles VALUES (?,?,?,?,?)',
                           (max_id, siteId, time_stamp, categoryId, url))
            return max_id
        return articleId[0]

    def saveWords(self, words, articelId):
        for word in words:

            max_id = self.c.execute('SELECT max(id) FROM words').fetchone()[0]
            if max_id:
                max_id += 1
            else:
                max_id = 1
            self.c.execute('INSERT INTO words VALUES (?, ?, ?)', (max_id, articelId, word))

    def commitAllChanges(self):
        self.conn.commit()


if __name__ == "__main__":
    modell = Model()
    # print(modell.getFeedCategores(0))
