import argparse
import json
import os
from google.cloud import language_v1
import numpy

def classify(text, verbose=True):
    """Classify the input text into categories."""

    language_client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
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
client = language_v1.LanguageServiceClient()

# The text to analyze
text = "Immigration is a complex and multifaceted phenomenon that has played a pivotal role in shaping societies throughout history. It involves the movement of individuals from one country to another with the intent of establishing residence. People migrate for various reasons, including economic opportunities, fleeing persecution, or seeking a better quality of life. Immigration brings diversity to communities, contributing to cultural richness and fostering innovation. However, it also raises challenges related to integration, social cohesion, and resource distribution. Striking a balance between welcoming newcomers and addressing the concerns of host populations is crucial for creating inclusive and sustainable societies. Ultimately, a thoughtful and compassionate approach to immigration can lead to the building of stronger, more resilient communities on a global scale."
document = language_v1.types.Document(
    content=text, type_=language_v1.types.Document.Type.PLAIN_TEXT
)

# Detects the sentiment of the text
sentiment = client.analyze_sentiment(
    request={"document": document}
).document_sentiment


result = classify(text, verbose=False)


print(f"Text: {text}")
print(f"Sentiment: {sentiment.score}, {sentiment.magnitude}")
print(result)




