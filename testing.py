import argparse
import json
import os
from google.cloud import language_v2
import numpy

def classify(text, verbose=True):
    """Classify the input text into categories."""

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

# Instantiates a client
client = language_v2.LanguageServiceClient()
# The text to analyze
text = "National Trafficking and Modern Slavery Pre- vention Month: Senate agreed to S. Res. 541, sup- porting the observation of National Trafficking and Modern Slavery Prevention Month during the period beginning on January 1, 2024, and ending on Feb- ruary 1, 2024, to raise awareness of, and opposition to, human trafficking and modern slavery."

result = classify(text, verbose=False)
print("You wrote: ", text)
print("Content Analysis: ",result)
print("")
print("")
for category, confidence in result.items():
    print(f"{category}: {confidence}")





