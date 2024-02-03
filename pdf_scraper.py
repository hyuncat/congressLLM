import requests
from bs4 import BeautifulSoup
import os

base_url = "https://www.senate.gov/legislative/LIS/floor_activity/all-floor-activity-files.htm"
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find links to PDFs
pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('dailydigest.pdf')]
for i in range(10):
    print(pdf_links[i])
    

# # Download PDFs
# for pdf_link in pdf_links:
#     pdf_url = f"https://www.senate.gov{pdf_link}"
#     pdf_filename = os.path.basename(pdf_url)
#     with open(pdf_filename, 'wb') as pdf_file:
#         pdf_file.write(requests.get(pdf_url).content)

# import pdfplumber

# def extract_text_from_pdf(pdf_path):
#     with pdfplumber.open(pdf_path) as pdf:
#         text = ""
#         for page in pdf.pages:
#             text += page.extract_text()
#     return text

# for pdf_link in pdf_links:
#     pdf_url = pdf_link if pdf_link.startswith('https://www.senate.gov') else f"https://www.senate.gov{pdf_link}"
#     pdf_filename = os.path.basename(pdf_url)
    
#     try:
#         response = requests.get(pdf_url)
#         response.raise_for_status()  # Check if the request was successful
#     except requests.exceptions.RequestException as e:
#         print(f"Error downloading PDF from {pdf_url}: {e}")
#         continue
    
#     with open(pdf_filename, 'wb') as pdf_file:
#         pdf_file.write(response.content)
#     pdf_text = extract_text_from_pdf(pdf_filename)

#     print(pdf_text[0])




# import mysql.connector

# Connect to Google Cloud SQL
# db_connection = mysql.connector.connect(
#     host='your_database_ip',
#     user='your_database_user',
#     password='your_database_password',
#     database='your_database_name'
# )

# cursor = db_connection.cursor()

# Insert data into the database
# for pdf_link in pdf_links:
#     pdf_url = f"https://www.senate.gov{pdf_link}"
#     pdf_filename = os.path.basename(pdf_url)
#     with open(pdf_filename, 'wb') as pdf_file:
#         pdf_file.write(requests.get(pdf_url).content)

#     # Extract text from PDF
#     pdf_text = extract_text_from_pdf(pdf_filename)

#     # Insert text into the database
#     insert_query = "INSERT INTO your_table_name (pdf_url, pdf_text) VALUES (%s, %s)"
#     cursor.execute(insert_query, (pdf_url, pdf_text))

# # Commit changes and close the connection
# db_connection.commit()
# cursor.close()
# db_connection.close()
