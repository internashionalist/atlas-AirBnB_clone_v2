#!/usr/bin/python3
"""
This module starts a Flask web application.
"""

from flask import Flask
from flask import render_template

app = Flask(__name__)

"""
Routing for application
"""


@app.route("/", strict_slashes=False)
def hello_hbnb():
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_rte(text):
    return "C {}".format(text.replace("_", " "))


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_rte(text="is cool"):
    return "Python {}".format(text.replace("_", " "))


@app.route("/number/<int:n>", strict_slashes=False)
def number_rte(n):
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    return render_template("5-number.html", n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_or_even(n):
    value = "even" if n % 2 == 0 else "odd"
    return render_template("6-number_odd_or_even.html", n=n, value=value)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
