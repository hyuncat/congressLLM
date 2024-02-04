import requests
from google.api_core.client_options import ClientOptions
from google.cloud import documentai
import pandas as pd

PROJECT_ID = "linen-marking-413218"
LOCATION = "us"  # Format is 'us' or 'eu'
PROCESSOR_ID = "16b9917b8213d461"  # Create processor in Cloud Console
MIME_TYPE = "application/pdf"

# Initialize Document AI client
client_options = {"api_endpoint": f"{LOCATION}-documentai.googleapis.com"}
client = documentai.DocumentProcessorServiceClient(
    client_options=client_options
)

# Function from https://medium.com/@mimichen123/document-ai-parsing-with-python-gcp-b3b38c2cbab9
def trim_text(text: str): 
    """ Removes spaces and newline characters. """ 
    return text.strip().replace("\n", " ")

def read_remote_pdf(url):
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
        result = client.process_document(request=request)

        document_object = result.document
        
        print("Document processing complete.")

        text = document_object.text
        text_blocks = []

        for page in document_object.pages:
            for block in page.blocks:
                startIndex = int(block.layout.text_anchor.text_segments[0].start_index)
                endIndex = int(block.layout.text_anchor.text_segments[0].end_index)
     
                subtext = trim_text(text[startIndex:endIndex])

                text_blocks.append(subtext)
            
        df = pd.DataFrame({'text_blocks': text_blocks})
        print(df)
        df.to_csv('output.csv', index=False)
        return df

df = read_remote_pdf('https://www.govinfo.gov/content/pkg/CREC-2024-01-31/pdf/CREC-2024-01-31-dailydigest.pdf')