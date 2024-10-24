#!/usr/bin/python3
"""
This module contains the tests for the console.
"""
import unittest
from unittest.mock import patch
from io import StringIO
import pycodestyle
import os
from console import HBNBCommand
from models.base_model import BaseModel
from models import storage


class TestConsole(unittest.TestCase):
    """
    Tests the console
    """
    def setUp(self):
        """
        Set up for tests
        """
        self.hbnbc = HBNBCommand()
        self.mock_stdout = StringIO()
        self.patched_stdout = patch('sys.stdout', new=self.mock_stdout)
        self.patched_stdout.start()

    def tearDown(self):
        """
        Cleans up post-test
        """
        self.patched_stdout.stop()
        self.mock_stdout.close()
        storage.reload()

    def test_pycode(self):
        """
        Tests for PEP8 compliance
        """
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0)

    def test_create(self):
        """
        Tests if create() creates an instance of BaseModel
        """
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            self.hbnbc.onecmd("create BaseModel")
            obj_id = mock_stdout.getvalue().strip()
            self.assertTrue(len(storage.all()) == 1)
            self.assertTrue(
                isinstance(storage.all()[f"BaseModel.{obj_id}"], BaseModel))

    def test_show(self):
        """
        Tests if show() prints string representation of an instance
        """
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.hbnbc.onecmd("create BaseModel")
            obj_id = mock_stdout.getvalue().strip()
            self.hbnbc.onecmd(f"show BaseModel {obj_id}")
            output = mock_stdout.getvalue().strip()
            self.assertNotEqual(output, "** no instance found **")

    def test_destroy(self):
        """
        Tests if destroy() deletes an instance
        """
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.hbnbc.onecmd("create BaseModel")
            obj_id = mock_stdout.getvalue().strip()
            self.hbnbc.onecmd(f"destroy BaseModel {obj_id}")
            self.hbnbc.onecmd(f"show BaseModel {obj_id}")
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "** no instance found **")

    def test_all(self):
        """
        Tests if all() prints all instances
        """
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.hbnbc.onecmd("create BaseModel")
            self.hbnbc.onecmd("all BaseModel")
            output = mock_stdout.getvalue().strip()
            self.assertNotEqual(output, "** no instance found **")

    def test_update(self):
        """
        Tests if update() updates an instance
        """
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.hbnbc.onecmd("create BaseModel")
            obj_id = mock_stdout.getvalue().strip()
            self.hbnbc.onecmd(f"update BaseModel {obj_id} name 'Wu'")
            self.hbnbc.onecmd(f"show BaseModel {obj_id}")
            output = mock_stdout.getvalue().strip()
            self.assertTrue("Wu" in output)

    def test_count(self):
        """
        Tests if count() counts the number of instances
        """
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            self.hbnbc.onecmd("create BaseModel")
            self.hbnbc.onecmd("create BaseModel")
            self.hbnbc.onecmd("count BaseModel")
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