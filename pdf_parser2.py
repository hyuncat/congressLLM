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


# Config variables
PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
LOCATION = "us"  # Format is 'us' or 'eu'
PROCESSOR_ID = os.environ.get('GCP_PROCESSOR_ID')  # Create processor in Cloud Console
MIME_TYPE = "application/pdf"

# Initialize Document AI client
client_options = {"api_endpoint": f"{LOCATION}-documentai.googleapis.com"}
document_client = documentai.DocumentProcessorServiceClient(client_options=client_options)


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
    
    # print(pdf_links)
    df = pd.DataFrame({'Date': pdf_dates, 'Link': pdf_links})
    # Write the concatenated DataFrame to a CSV file
    df.to_csv('./static/output.csv', index=False)
    return df

def trim_text(text: str): 
    """ Removes spaces and newline characters. """ 
    return text.strip().replace("\n", " ")

# Create database of Document AI generated snippets on all PDFs
def parse_pdf(url, date):

    # Download the PDF file from the URL
    response = requests.get(url)
    if response.status_code == 200:
        # Read file into memory
        pdf_content = response.content

        # Load Binary Data into Document AI RawDocument Object
        raw_document = documentai.RawDocument(
            content=pdf_content, 
            mime_type=MIME_TYPE
        )

        # Configure the process request
        parent = f"projects/{PROJECT_ID}/locations/{LOCATION}/processors/{PROCESSOR_ID}"
        request = {"name": parent, "raw_document": raw_document}

        # Use the Document AI client to process the sample form
        result = document_client.process_document(request=request)

        document_object = result.document
        
        print("Document processing complete.")

        text = document_object.text
        text_blocks = []
        date_vec = []

        for page in document_object.pages:
            for block in page.blocks:
                startIndex = int(block.layout.text_anchor.text_segments[0].start_index)
                endIndex = int(block.layout.text_anchor.text_segments[0].end_index)
     
                subtext = trim_text(text[startIndex:endIndex])

                text_blocks.append(subtext)
                date_vec.append(date)
            
        df = pd.DataFrame({
            'Paragraph': text_blocks,
            'Date': date_vec
        })
        df.to_csv('./static/docAI_parse.csv', index=False)
        return df
    
def create_data():
    # Create dataframe with PDF links and dates
    base_url = "https://www.senate.gov/legislative/LIS/floor_activity/all-floor-activity-files.htm"
    base_df = init_pdf_df(base_url)
    # Create database of Document AI generated snippets on all PDFs
    vec = []
    big_df = pd.DataFrame(columns=['Paragraph', 'Date'])
    for i in range(4):
        df = parse_pdf(base_df['Link'][i], base_df['Date'][i])
        big_df = pd.concat([big_df, df], ignore_index=True)
    
    big_df.to_csv('./static/full_data.csv', index=False)

    return big_df


# Run

#base_url = "https://www.senate.gov/legislative/LIS/floor_activity/all-floor-activity-files.htm"
#df = init_pdf_df(base_url)
#link = df['Link'][0]
#date = df['Date'][0]
#more_df = parse_pdf(link, date)
#print(more_df)

create_data()