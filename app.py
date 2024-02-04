import re
from datetime import datetime
import argparse
import json
import os
import csv
import numpy
from flask import Flask
from flask import render_template
from flask import request
def switch_counter(category, list):
    if category == "Agriculture":
        list[0] +=1
    elif category == "Civil Rights":
        list[1] +=1
    elif category == "Defense":
        list[1] +=1
    elif category == "Economy":
        list[1] +=1
    elif category == "Education":
        list[1] +=1
    elif category == "Energy":
        list[1] +=1
    elif category == "Environment":
        list[1] +=1
    elif category == "Foreign Policy":
        list[1] +=1
    elif category == "Health Care":
        list[1] +=1
    elif category == "Immigration":
        list[1] +=1
    elif category == "Infrastructure":
        list[1] +=1
    elif category == "Judicial Sytem":
        list[1] +=1
    elif category == "Labor":
        list[1] +=1
    elif category == "National Security":
        list[1] +=1
    elif category == "Trade":
        list[1] +=1
    elif category == "Transportation":
        list[1] +=1
    elif category == "Social Welfare":
        list[1] +=1
    elif category == "Veteran's Affairs":
        list[1] +=1

"""""
# Step 1: Open the CSV file
with open('INSERT_SARAH_DATABASE.csv', 'r') as file:
    # Step 2: Create a CSV reader
    csv_reader = csv.reader(file)
    
    # Step 3: Convert the CSV data into a list of lists
    data_list = list(csv_reader)

# Step 4: Convert the list of lists into a NumPy array
data_matrix = np.array(data_list)
"""
app = Flask(__name__)

def search_proceedings(query, search_type):
    results = []
    i = 0
    # Implement your search logic here
    if search_type=="relevance":
        for row in data_matrix:
            for category, confidence in row[4].items:
                if category == query:
                    results[i] = {'title': row[3], 'content': row[1]}
                    i+=1

        return results
   # elif search_type=="date":

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
    search_type = request.args.get('queryoptions')
   

    # Call your search algorithm function
    results = search_proceedings(query, search_type)

    # Render the template with the search results
    return render_template("search_results.html", query=query, results=results)



if __name__ == '__main__':
    app.run(debug=True)
