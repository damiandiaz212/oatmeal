import sqlite3

class Database:
    def __init__(self, path):
        self.connection = sqlite3.connect(path, check_same_thread=False, isolation_level=None)
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE if not exists portfolio (id TEXT PRIMARY KEY, name TEXT, starting REAL, buying_power REAL, balance REAL, adj REAL, portfolio TEXT)")
    def save(self, image):
        query = f"""
                INSERT INTO portfolio VALUES('{image.id}', '{image.name}', {image.starting}, {image.buying_power}, {image.balance}, {image.adj}, '{image.portfolio}')
                    ON CONFLICT(id) DO UPDATE SET
                        starting={image.starting},
                        buying_power={image.buying_power},
                        balance={image.balance},
                        adj={image.adj},
                        portfolio='{image.portfolio}'
                """
        return self.execute_query('INSERT', query)
    def load_all(self):
        query = "SELECT * FROM portfolio"
        return self.execute_query('SELECT', query)
    def delete(self, id):
        query = f"""
                DELETE FROM portfolio
                WHERE id='{id}'
                """
        return self.execute_query('DELETE', query)
    def execute_query(self, statement, query):
        try:
            return self.cursor.execute(query)
        except Exception as e:
            print(f'Failed to execute {statement} to db: ', e)
            return {}, 500
    def disconnect(self):
        self.connection.close()