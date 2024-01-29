import psycopg2

class PortfolioDB:
    def __init__(self, db_path):
        self.connection = psycopg2.connect(db_path, sslmode='require')
        self.connection.autocommit = True
        self.create_table()
    def __del__(self):
        self.connection.close()
    def create_table(self):
        query = "CREATE TABLE if not exists portfolio (id TEXT PRIMARY KEY, name TEXT, starting REAL, buying_power REAL, balance REAL, adj REAL, portfolio TEXT)"
        self.execute_query(query)
    def create_entry(self, image):
        query = "INSERT INTO portfolio VALUES(%s, %s, %s, %s, %s, %s, %s)"
        values = (image.id, image.name, image.starting, image.buying_power, image.balance, image.adj, image.portfolio)
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        self.connection.commit()
    def update_entry(self, image):
        query = f"UPDATE portfolio SET buying_power = {image.buying_power}, balance = {image.balance}, adj = {image.adj}, portfolio = '{image.portfolio}' WHERE id = '{image.id}'"
        self.execute_query(query)
    def load_all(self):
        query = "SELECT * FROM portfolio"
        return self.execute_query(query).fetchall()
    def delete(self, id):
        query = f"DELETE FROM portfolio WHERE id={id}"
        self.execute_query(query)
    def clear(self):
        query = "DELETE FROM portfolio"
        self.execute_query(query)
    def execute_query(self, statement):
        try:
            cursor = self.connection.cursor()
            cursor.execute(statement)
            self.connection.commit()
            return cursor
        except Exception as e:
            print(f'Failed to execute {statement} to db: ', e)
            return {}, 500