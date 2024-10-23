#!/usr/bin/python3
"""
This module initializes the appropriate storage engine.
"""

from os import getenv


if getenv("HBNB_TYPE_STORAGE") == "db":  # database storage
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:  # file storage
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()  # reloads objects from file or database