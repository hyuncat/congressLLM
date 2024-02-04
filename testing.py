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
text = "SALT MARRIAGE PENALTY ELIMINATION ACT; DENOUNCING THE HARMFUL, ANTI- AMERICAN ENERGY POLICIES OF THE BIDEN ADMINISTRATION"




result = classify(text, verbose=False)

print(result)




