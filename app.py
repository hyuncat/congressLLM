import re
from datetime import datetime
import argparse
import json
import os
import numpy

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')
from io import BytesIO
import base64

from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)

def search_proceedings(query):
    # Implement your search logic here
    # if query == "Business":
    #     return [{'title': 'You picked Business!', 'content': 'Details for Business'}]
    # You can use the selected_category and query to filter and rank proceedings
    # Return a list of relevant proceedings based on your logic
    # For now, just returning a sample list

    # return results

    return [{'title': 'Proceeding 1', 'content': 'Details for Proceeding 1'},
            {'title': 'Proceeding 2', 'content': 'Details for Proceeding 2'}]

@app.route("/")
def home():
    # call function to get top issues
    top_ten_list = get_top_ten_list()
    # Generate Matplotlib plot
    data = [1, 2, 2, 3, 3, 3, 4, 4, 5]
    plt.hist(data, bins=5)
    plt.xlabel('Values')
    plt.ylabel('Frequency')

    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    # Convert the plot to base64 for embedding in HTML
    plot_data = base64.b64encode(img.getvalue()).decode()
    return render_template("home.html", top_ten_list=top_ten_list, plot_data=plot_data)

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

# Hello route
# @app.route("/hello/")
# @app.route("/hello/<name>")
# def hello_there(name=None):
#     return render_template (
#         "hello_there.html",
#         name=name,
#         date=datetime.now()
#     )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

@app.route("/search")
def search():
    query = request.args.get('query')

    # Call search algorithm function
    results = search_proceedings(query)

    # Render the template with the search results
    return render_template("search_results.html", query=query, results=results)

# @app.route('/histogram')
# def histogram():
#     # Generate Matplotlib plot
#     data = [1, 2, 2, 3, 3, 3, 4, 4, 5]
#     plt.hist(data, bins=5)
#     plt.xlabel('Values')
#     plt.ylabel('Frequency')

#     # Save the plot to a BytesIO object
#     img = BytesIO()
#     plt.savefig(img, format='png')
#     img.seek(0)
#     plt.close()

#     # Convert the plot to base64 for embedding in HTML
#     plot_data = base64.b64encode(img.getvalue()).decode()

#     return render_template('histogram.html', plot_data=plot_data)

def get_top_ten_list():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


if __name__ == '__main__':
    app.run(debug=True)
