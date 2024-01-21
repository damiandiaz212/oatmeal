import sqlite3

class Database:
    def __init__(self, path):
        connection = sqlite3.connect(path, check_same_thread=False, isolation_level=None)
        self.cursor = connection.cursor()
        self.cursor.execute("CREATE TABLE if not exists portfolio (id TEXT, name TEXT, starting REAL, buying_power REAL, balance REAL, adj REAL, portfolio TEXT)")
    def save(self, image):
        try:
            self.cursor.execute(f"INSERT INTO portfolio VALUES ('{image.id}', '{image.name}', {image.starting}, {image.buying_power}, {image.balance}, {image.adj}, '{image.portfolio}')")
        except Exception as e:
            print('Failed to save portoflio to db: ', e)
    def load_all(self):
        rows = self.cursor.execute("SELECT * FROM portfolio").fetchall()
        print(rows)
        return rows
    def clear(self):
        pass