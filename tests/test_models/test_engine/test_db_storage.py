#!/usr/bin/python3
"""
This module contains tests for the DBStorage class.
"""
import unittest
from models.engine.db_storage import DBStorage
from models.user import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os


class test_DBStorage(unittest.TestCase):
    """
    Tests the DBStorage class
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up for tests
        """
        os.environ["HBNB_ENV"] = "test"
        os.environ["HBNB_MYSQL_USER"] = "RZA"
        os.environ["HBNB_MYSQL_PWD"] = "WuTang"
        os.environ["HBNB_MYSQL_HOST"] = "localhost"
        os.environ["HBNB_MYSQL_DB"] = "WuTangClan"

        cls.storage = DBStorage()
        cls.storage.reload()
        cls.session = cls.storage._DBStorage__session

    @classmethod
    def tearDownClass(cls):
        """
        Cleans up post-test
        """
        cls.session.close()
        del os.environ["HBNB_ENV"]
        del os.environ["HBNB_MYSQL_USER"]
        del os.environ["HBNB_MYSQL_PWD"]
        del os.environ["HBNB_MYSQL_HOST"]
        del os.environ["HBNB_MYSQL_DB"]

    def test_all(self):
        """
        Tests if all() returns __objects
        """
        obj = self.storage.all()
        obj_storage = self.storage._DBStorage__session
        self.assertIsNotNone(obj)
        self.assertEqual(type(obj), dict)
        self.assertIs(obj, obj_storage)

    def test_new(self):
        """
        Tests if new() adds an object to __objects
        """
        user = User(email="test@wutang.com", password="protectyaneck")
        self.storage.new(user)
        self.assertIn(user, self.session.new)

    def test_save(self):
        """
        Tests if save() saves the session
        """
        user = User(email="save_test@wutang.com", password="36chambers")
        self.storage.new(user)
        self.storage.save()
        self.assertIn(user, self.session)

    def test_delete(self):
        """
        Tests if delete() deletes an object from __objects
        """
        user = User(email="delete_test@wutang.com", password="forever")
        self.storage.new(user)
        self.storage.save()
        self.storage.delete(user)
        self.storage.save()
        obj_dict = self.storage.all("User")
        self.assertNotIn(f"User.{user.id}", obj_dict)

    def test_reload(self):
        """
        Tests if reload() loads objects from the database
        """
        self.storage.reload()
        obj_dict = self.storage.all()
        self.assertIsInstance(obj_dict, dict)


if __name__ == "__main__":
    unittest.main()
