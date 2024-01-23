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
        cls.temp_db_path = 'test/temp_database.db'
        cls.mock_db_path = 'test/mock_database.db'
        cls.mock_db = Database(cls.mock_db_path)

    @classmethod
    def tearDownClass(cls):
        cls.mock_db.disconnect()
       
    def test_save_and_load_all(self):
        
        temp_db = Database(self.temp_db_path)

        test_image = MockImage('1', 'Test Image', 100.0, 200.0, 300.0, 1.0, 'test_portfolio')
        temp_db.save(test_image)

        loaded_images = temp_db.load_all().fetchall()
        self.assertEqual(len(loaded_images), 1)
        self.assertEqual(loaded_images[0], (test_image.id, test_image.name, test_image.starting, test_image.buying_power, test_image.balance, test_image.adj, test_image.portfolio))

        temp_db.disconnect()
        os.remove(self.temp_db_path)

    def test_delete(self):
      
        test_image = MockImage('2', 'Test Image 2', 100.0, 200.0, 300.0, 1.0, 'test_portfolio2')
        self.mock_db.save(test_image)

        self.mock_db.delete('2')
        loaded_images = self.mock_db.load_all().fetchall()
        self.assertEqual(len(loaded_images), 1)