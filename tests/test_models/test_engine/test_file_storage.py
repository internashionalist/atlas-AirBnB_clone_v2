#!/usr/bin/python3
"""
This module contains tests for the FileStorage module.
"""
import unittest
import pycodestyle
import os
from models.user import User
from models.engine.file_storage import FileStorage


class test_fileStorage(unittest.TestCase):
    """
    Tests the FileStorage module
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up for tests
        """
        cls.storage = FileStorage()
        cls.user = User()
        cls.user.first_name = "Wu"
        cls.user.last_name = "Tang"
        cls.user.email = "protectyaneck@gmail.com"

    @classmethod
    def tearDownClass(cls):
        """
        Cleans up post-test
        """
        del cls.user
        del cls.storage

    def tearDown(self):
        """
        Removes JSON file
        """
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_all(self):
        """
        Tests if all() returns __objects
        """
        obj = self.storage.all()
        obj_storage = self.storage._FileStorage__objects
        self.assertIsNotNone(obj)
        self.assertEqual(type(obj), dict)
        self.assertIs(obj, obj_storage)

    def test_new(self):
        """
        Tests if new() adds an object to __objects
        """
        storage = FileStorage()
        user = User()
        user.id = "88675309"
        user.name = "Wu"
        storage.new(user)
        obj = storage.all()
        key = user.__class__.__name__ + "." + str(user.id)
        self.assertIsNotNone(obj[key])

    def test_save(self):
        """
        Tests if save() saves objects to file
        """
        self.storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """
        Tests if reload() loads objects from file
        """
        self.storage.save()
        self.storage.reload()
        obj = self.storage.all()
        self.assertIsNotNone(obj)
    
    def test_delete(self):
        """
        Tests if delete() deletes objects from __objects
        """
        storage = FileStorage()
        user = User()
        user.id = "88675309"
        user.name = "Wu"
        storage.new(user)
        key = user.__class__.__name__ + "." + str(user.id)
        storage.delete(user)
        obj = storage.all()
        self.assertNotIn(key, obj)


if __name__ == "__main__":
    unittest.main()
