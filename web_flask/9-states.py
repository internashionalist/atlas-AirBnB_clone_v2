#!/usr/bin/python3
"""
This module starts a Flask web application.
"""

from models import storage
from flask import Flask, render_template
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Closes database session
    """
    storage.close()


@app.route("/states", strict_slashes=False)
def states_list():
    """
    Lists all states in the database
    """
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template("7-states_list.html", states=sorted_states)


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """
    Renders id of state from database to this route
    """
    states = storage.all(State).values()
    current_state = None
    for state in states:
        if state.id == id:
            current_state = state
            current_state.cities.sort(key=lambda city: city.name)
            break

    if current_state is None:
        current_state = "not found!"

    return render_template("9-states.html", state=current_state)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
