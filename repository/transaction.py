import psycopg2

class TransactionDB:
    def __init__(self, db_path):
        self.connection = psycopg2.connect(db_path, sslmode='require')
        self.connection.autocommit = True
        self.create_table()
    def __del__(self):
        self.connection.close()
    def create_table(self):
        query = "CREATE TABLE IF NOT EXISTS transaction (id TEXT NOT NULL, type TEXT NOT NULL, symbol TEXT NOT NULL, amount REAL NOT NULL, price REAL NOT NULL, timestamp TEXT NOT NULL);"
        self.execute_query(query)
    def append_entry(self, values):
        query = "INSERT INTO transaction VALUES(%s, %s, %s, %s, %s, %s)"
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        self.connection.commit()
    def fetch_all_by_id(self, id):
        query = f"SELECT * FROM transaction WHERE id='{id}'"
        return self.execute_query(query).fetchall()
    def purge(self, id):
        query = f"DELETE FROM transaction WHERE id='{id}'"
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