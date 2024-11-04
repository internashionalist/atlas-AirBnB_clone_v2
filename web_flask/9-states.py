#!/usr/bin/python3
"""
This module starts a Flask web application.
"""

from models import storage
from flask import Flask, render_template
from models.state import State
from models.city import City

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
    states_dict = storage.all(State)
    all_states = []
    for key, value in states_dict.items():
        all_states.append(value)
    return render_template("9-states.html", all_states=all_states)


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """
    Lists all states in the database
    """
    states_dict = storage.all(State)
    all_states = []
    states_id = []
    for key, value in states_dict.items():
        all_states.append(value)
        states_id.append(value.id)
    return render_template("9-states.html", all_states=all_states,
                           states_id=states_id, id=id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
