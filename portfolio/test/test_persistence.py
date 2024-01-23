import unittest
import sqlite3
import os
from service.persistence import Database

class MockImage:
    def __init__(self, id, name, starting, buying_power, balance, adj, portfolio):
        self.id = id
        self.name = name
        self.starting = starting
        self.buying_power = buying_power
        self.balance = balance
        self.adj = adj
        self.portfolio = portfolio

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_path = 'test/test_database.db'
        cls.db = Database(cls.db_path)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.db_path)

    def test_save_and_load_all(self):
        # Testing both save and load_all methods
        test_image = MockImage('1', 'Test Image', 100.0, 200.0, 300.0, 1.0, 'test_portfolio')
        self.db.save(test_image)

        loaded_images = self.db.load_all().fetchall()
        self.assertEqual(len(loaded_images), 1)
        self.assertEqual(loaded_images[0], (test_image.id, test_image.name, test_image.starting, test_image.buying_power, test_image.balance, test_image.adj, test_image.portfolio))

    def test_delete(self):
        # Add a new item and then delete it
        test_image = MockImage('2', 'Test Image 2', 100.0, 200.0, 300.0, 1.0, 'test_portfolio2')
        self.db.save(test_image)

        self.db.delete('2')
        loaded_images = self.db.load_all().fetchall()
        self.assertEqual(len(loaded_images), 1)  # since we added one and deleted one, should still be one

if __name__ == '__main__':
    unittest.main()