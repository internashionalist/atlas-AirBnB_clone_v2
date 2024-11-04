#!/usr/bin/python3
"""
This module starts a Flask web application.
"""

from models import storage
from flask import Flask, render_template
from models.state import State
from models.amenity import Amenity

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Closes database session
    """
    storage.close()


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """
    Renders hbnb_filters page with sorted States and Amenities
    """
    states = sorted(storage.all(State).values(),
                    key=lambda state: state.name)
    amenities = sorted(storage.all(Amenity).values(),
                       key=lambda amenity: amenity.name)
    return render_template("10-hbnb_filters.html",
                           states=states, amenities=amenities)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
