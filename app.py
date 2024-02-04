import re
from datetime import datetime
import argparse
import json
import os
import numpy

from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)

def search_proceedings(query):
    # Implement your search logic here
    if query == "Business":
        return [{'title': 'You picked Business!', 'content': 'Details for Business'}]
    # You can use the selected_category and query to filter and rank proceedings
    # Return a list of relevant proceedings based on your logic
    # For now, just returning a sample list
    return [{'title': 'Proceeding 1', 'content': 'Details for Proceeding 1'},
            {'title': 'Proceeding 2', 'content': 'Details for Proceeding 2'}]

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
    selected_category = request.args.get('cars')

    # Call your search algorithm function
    results = search_proceedings(query)

    # Render the template with the search results
    return render_template("search_results.html", query=query, results=results)



if __name__ == '__main__':
    app.run(debug=True)
