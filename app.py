import re
from datetime import datetime
import argparse
import json
import os
import numpy

from flask import Flask, render_template, request


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

@app.route("/search")
def search():
    query = request.args.get('query')
    # Perform search logic here based on the query
    # Return the search results or render a new template
    return render_template("search_results.html", query=query)

if __name__ == '__main__':
    app.run(debug=True)
