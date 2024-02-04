import os
import argparse
import re

import requests
from bs4 import BeautifulSoup
import numpy
import pandas as pd
import json

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


# Classify the input text into categories.
def complex_classify(text, verbose=False):
    language_client = language_v2.LanguageServiceClient()

    document = language_v2.Document(
        content=text, type_=language_v2.Document.Type.PLAIN_TEXT
    )
    response = language_client.classify_text(request={"document": document})
    categories = response.categories

    result = {}

    for category in categories:
        # Turn the categories into a dictionary of the form:
        # {category.name: category.confidence}, so that they can
        # be treated as a sparse vector.
        result[category.name] = category.confidence

    if verbose:
        print(text)
        for category in categories:
            print("=" * 20)
            print("{:<16}: {}".format("category", category.name))
            print("{:<16}: {}".format("confidence", category.confidence))

    return result


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
        complex_cat = []
        simple_cat = []

        simple_keys = pd.read_csv('./static/categoryreduction.csv', header=0)
        count = 1
        for page in document_object.pages:
            for block in page.blocks:
                startIndex = int(block.layout.text_anchor.text_segments[0].start_index)
                endIndex = int(block.layout.text_anchor.text_segments[0].end_index)
     
                subtext = trim_text(text[startIndex:endIndex])

                super_subtext = subtext.split()
                if len(super_subtext) < 10:
                    continue

                try:
                    c_cat = complex_classify(subtext, verbose=False)
                except:
                    continue

                s_cat = {}

                # Create dictionary of new simple categories + confidence values
                for key in c_cat:
                    print(key)
                    s_cat_row = simple_keys[simple_keys['complex'] == key]
                    
                    if s_cat_row.empty:
                        continue

                    s_cat_row = s_cat_row.iloc[0]
                    print(s_cat_row)
                    s_cat_key = s_cat_row['simple']
                    s_cat.update({s_cat_key: c_cat[key]}) # Append key value pair to dictionary

                # Create dictionary of new simple categories + confidence values
                #s_cat_row = simple_keys[simple_keys['complex'] == c_cat]
                #s_cat_key = s_cat_row['simple'].values[0]
                #s_cat = {s_cat_key: c_cat[c_cat[s_cat_row['complex'].values[0]]]}

                text_blocks.append(subtext)
                date_vec.append(date)
                complex_cat.append(json.dumps(c_cat))
                simple_cat.append(json.dumps(s_cat))

                print(f"Block {count} read.")
                count += 1

            
        df = pd.DataFrame({
            'Paragraph': text_blocks,
            'Date': date_vec,
            'ComplexCategory': complex_cat,
            'SimpleCategory': simple_cat
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

df = create_data()