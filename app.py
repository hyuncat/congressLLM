import re
from datetime import datetime
import argparse
import json
import os
import numpy as np
import csv

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')
from io import BytesIO
import base64

from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)

with open('static/full_data.csv', 'r') as file:
    # Step 2: Create a CSV reader
    csv_reader = csv.reader(file)

    # Step 3: Convert the CSV data into a list of lists
    data_list = list(csv_reader)

# Step 4: Convert the list of lists into a NumPy array
data_matrix = np.array(data_list)
for row in data_matrix:
    if row[3][0] == '{':
        np.delete(row[3],0)

def formatComplex(text):
    match = re.search(r"'(.*?)'", text)
    if match:
        extracted_text = match.group(1)  # Extracted text within single quotes
        # Replace slashes with comma + space
        modified_text = re.sub(r'/', ', ', extracted_text)
        return modified_text
    else:
        return

def search_proceedings(query, search_type):
    results = []
    relev = {}
    if search_type=="relevance":
        for row in data_matrix:
            if query in row[3]:
                    results.append({'title': formatComplex(row[2]), 'content': row[0]})
                    conf_str = re.search(r'(?<=:\s)(\d+\.\d+)', row[2])
                    if conf_str:
                        conf = float(conf_str.group())
                        relev[row[0]] = conf

        # Sort results based on relevance score
        results.sort(key=lambda x: relev.get(x['content'], 0), reverse=False)
        return results

    elif search_type=="date":
        return

    # return [{'title': 'Proceeding 1', 'content': 'Details for Proceeding 1'},
            # {'title': 'Proceeding 2', 'content': 'Details for Proceeding 2'}]

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

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

@app.route("/search")
def search():
    query = request.args.get('query')
    search_type = request.args.get('queryoptions')
   

    # Call your search algorithm function
    results = search_proceedings(query, search_type)

    # Render the template with the search results
    return render_template("search_results.html", query=query, search_type=search_type, results=results)

def get_top_ten_list():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


if __name__ == '__main__':
    app.run(debug=True)


