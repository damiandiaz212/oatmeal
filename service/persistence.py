import sqlite3

class Database:
    def __init__(self, path):
        self.path = path
        self.connection = sqlite3.connect(self.path, check_same_thread=False, isolation_level=None)
        self.create_table()
    def __del__(self):
        self.connection.close()
    def create_table(self):
        query = "CREATE TABLE if not exists portfolio (id TEXT PRIMARY KEY, name TEXT, starting REAL, buying_power REAL, balance REAL, adj REAL, portfolio TEXT)"
        return self.execute_query('CREATE', query)
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
            result = self.connection.cursor().execute(query)
            return result
        except Exception as e:
            print(f'Failed to execute {statement} to db: ', e)
            return {}, 500