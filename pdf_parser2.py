import os
import argparse
import re

import requests
from bs4 import BeautifulSoup
import numpy
import pandas as pd

from google.api_core.client_options import ClientOptions
from google.cloud import documentai
from google.cloud import language_v2


# Create dataframe with PDF links and dates
def init_pdf_df(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('dailydigest.pdf')]
    table = pd.read_html(base_url)
    cattable = pd.concat(table)

    pdf_dates = []
    for i in range(len(pdf_links)):
        date = table[0].iloc[i, 0]
        match = re.search(r"\b\d{4}\b", date)
        if match:
            date = date[:match.start()+4]
            
        pdf_dates.append(date)
    
    df = pd.DataFrame({'Date': pdf_dates, 'Link': pdf_links})
    # Write the concatenated DataFrame to a CSV file
    df.to_csv('output.csv', index=False)
    return df

base_url = "https://www.senate.gov/legislative/LIS/floor_activity/all-floor-activity-files.htm"
df = init_pdf_df(base_url)


# Find links to PDFs (daily digest only)
# pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('dailydigest.pdf')]
# for i in range(10):
#     print(pdf_links[i])

