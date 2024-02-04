import re
from datetime import datetime
import argparse
import json
import os
import numpy
import csv
import numpy as np
import pandas as pd
from vertexai.preview.language_models import TextGenerationModel
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')
from io import BytesIO
import base64

from flask import Flask
from flask import render_template
from flask import request

def interview(text ,temperature: float = .2,):
    """Ideation example with a Large Language Model"""

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": temperature,
        "max_output_tokens": 75,
        "top_p": .8,
        "top_k": 40,
    }

    model = TextGenerationModel.from_pretrained("text-bison@002")
    response = model.predict(
        text,
        **parameters,
    )
    return response.text

def switch_counter(category, list):
    if category == "Agriculture":
        list[0] +=1
    elif category == "Civil Rights":
        list[1] +=1
    elif category == "Defense":
        list[2] +=1
    elif category == "Economy":
        list[3] +=1
    elif category == "Education":
        list[4] +=1
    elif category == "Energy":
        list[5] +=1
    elif category == "Environment":
        list[6] +=1
    elif category == "Foreign Policy":
        list[7] +=1
    elif category == "Health Care":
        list[8] +=1
    elif category == "Immigration":
        list[9] +=1
    elif category == "Infrastructure":
        list[10] +=1
    elif category == "Judicial Sytem":
        list[11] +=1
    elif category == "Labor":
        list[12] +=1
    elif category == "National Security":
        list[13] +=1
    elif category == "Taxation":
        list[14] +=1
    elif category == "Technology":
        list[15] +=1
    elif category == "Trade":
        list[16] +=1
    elif category == "Transportation":
        list[17] +=1
    elif category == "Social Welfare":
        list[18] +=1
    elif category == "Veterans Affairs":
        list[19] +=1


counter_list = [0]*20


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

def search_proceedings(query, search_type):
    results = []
   
    if search_type=="relevance":
        for row in data_matrix:
            if row[3].find(query):
                    results.append({'title': query , 'content': row[0]})
                    switch_counter(query,counter_list)
                    

                    
                    

        return results
    elif search_type=="date":
        return



topic_list = ["Agriculture", "Civil Rights", "Defense","Economy","Education","Energy" , "Environment", "Foreign Policy" ,"Healthcare", "Immigration", "Infrastructure", "Judicial System", "Labor", "National Security", "Taxation", "Technology", "Trade", "Transportation", "Social Welfare", "Veterans Affairs"]

@app.route("/")
def home():
    # call function to get top issues
    top_ten_list = get_top_ten_list()
    # Generate Matplotlib plot
    data = [1, 2, 2, 3, 3, 3, 4, 4, 5]
    plt.hist(data, bins=5)
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    topic_index = max(counter_list)
    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    topic = topic_list[topic_index]

    summary = interview(f"Give me a quick summary about {topic} in the modern American Political Scene" )
    # Convert the plot to base64 for embedding in HTML
    plot_data = base64.b64encode(img.getvalue()).decode()
    return render_template("home.html",  plot_data=plot_data, topic = topic, summary = summary)

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
    results =search_proceedings(query, search_type)

    # Render the template with the search results
    return render_template("search_results.html", query=query, search_type=search_type, results=results)

def get_top_ten_list():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


if __name__ == '__main__':
    app.run(debug=True)
