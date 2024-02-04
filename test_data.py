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
    elif category == "Veteran's Affairs":
        list[19] +=1

"""""
"""
app = Flask(__name__)

with open('static/full_data.csv', 'r') as file:
    # Step 2: Create a CSV reader
    csv_reader = csv.reader(file)

    # Step 3: Convert the CSV data into a list of lists
    data_list = list(csv_reader)

# Step 4: Convert the list of lists into a NumPy array
data_matrix = np.array(data_list)

for row in data_matrix:
    print(row[3])