import re
from datetime import datetime
import argparse
import json
import os
import numpy

from google.cloud import language_v1
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

# Hello route
@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name=None):
    return render_template (
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

if __name__ == '__main__':
    app.run(debug=True)
