#!/usr/bin/python3
"""
This module starts a Flask web application.
"""

from models import storage
from flask import Flask, render_template
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(self):
    """
    Closes database session
    """
    storage.close()


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """
    Returns list of cities by state
    """
    states = storage.all(State).values()

    for state in states:
        state.cities.sort(key=lambda city: city.name)

    return render_template("8-cities_by_states.html", states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
