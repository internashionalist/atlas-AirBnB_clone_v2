#!/usr/bin/python3
"""
This module contains the tests for the console.
"""
import unittest
from unittest.mock import patch
from io import StringIO
import pycodestyle
from console import HBNBCommand
from models import storage
from models.user import User
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
import os


class TestConsole(unittest.TestCase):
    """
    Tests the console
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up environment for tests
        """
        cls.hbnbc = HBNBCommand()

    def setUp(self):
        """
        Set up pre-test
        """
        self.mock_stdout = StringIO()
        self.patched_stdout = patch('sys.stdout', new=self.mock_stdout)
        self.patched_stdout.start()
        storage.reload()

    def tearDown(self):
        """
        Cleans up post-test
        """
        self.patched_stdout.stop()
        self.mock_stdout.close()
        if isinstance(storage, DBStorage):
            storage._DBStorage__session.close()
        else:
            storage._FileStorage__objects = {}

    def test_pycode(self):
        """
        Tests for pycode compliance
        """
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0)

    def test_create(self):
        """
        Tests if create() creates an instance of User
        """
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.hbnbc.onecmd("create User email='protectyaneck@gmail.com' \
                              password='suuu' first_name='Wu' last_name='Tang'")
            obj_id = mock_stdout.getvalue().strip()
            stored_obj = storage.all().get(f"User.{obj_id}")
            self.assertIsNotNone(stored_obj)
            self.assertTrue(isinstance(stored_obj, User))

    def test_show(self):
        """
        Tests if show() prints string representation of an instance
        """
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.hbnbc.onecmd("create User email='protectyaneck@gmail.com' \
                              password='suuu' first_name='Wu' last_name='Tang'")
            obj_id = mock_stdout.getvalue().strip()
            self.hbnbc.onecmd(f"show User {obj_id}")
            output = mock_stdout.getvalue().strip()
            self.assertNotEqual(output, "** no instance found **")
            self.assertIn(f"{obj_id}", output)

    def test_destroy(self):
        """
        Tests if destroy() deletes an instance
        """
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.hbnbc.onecmd("create User email='protectyaneck@gmail.com' \
                              password='suuu' first_name='Wu' last_name='Tang'")
            obj_id = mock_stdout.getvalue().strip()
            self.hbnbc.onecmd(f"destroy User {obj_id}")
            self.hbnbc.onecmd(f"show User {obj_id}")
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, f"{obj_id} deleted")

    def test_all(self):
        """
        Tests if all() prints all instances
        """
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.hbnbc.onecmd("create User email='protectyaneck@gmail.com' \
                              password='suuu' first_name='Wu' last_name='Tang'")
            self.hbnbc.onecmd("all User")
            output = mock_stdout.getvalue().strip()
            self.assertNotEqual(output, "** no instance found **")
            self.assertIn("User", output)

    def test_update(self):
        """
        Tests if update() updates an instance
        """
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.hbnbc.onecmd("create User email='protectyaneck@gmail.com' \
                              password='suuu' first_name='Wu' last_name='Tang'")
            obj_id = mock_stdout.getvalue().strip()
            self.hbnbc.onecmd(f"update User {obj_id} name 'Wu'")
            self.hbnbc.onecmd(f"show User {obj_id}")
            output = mock_stdout.getvalue().strip()
            self.assertTrue("Wu" in output)

    def test_count(self):
        """
        Tests if count() counts the number of instances
        """
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.hbnbc.onecmd("create User email='protectyaneck@gmail.com' \
                              password='suuu' first_name='Wu' last_name='Tang'")
            self.hbnbc.onecmd("count User")
            output = mock_stdout.getvalue().strip()
            self.assertTrue("2" in output)

    def test_quit(self):
        """
        Tests if quit() exits the console
        """
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.hbnbc.onecmd("quit")
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "")

    def test_EOF(self):
        """
        Tests if EOF exits the console
        """
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.hbnbc.onecmd("EOF")
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "")


if __name__ == "__main__":
    unittest.main()
