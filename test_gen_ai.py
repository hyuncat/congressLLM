from vertexai.preview.language_models import TextGenerationModel

def interview(temperature: float = .2):
    """Ideation example with a Large Language Model"""

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": temperature,
        "max_output_tokens": 256,
        "top_p": .8,
        "top_k": 40,
    }

    model = TextGenerationModel.from_pretrained("text-bison@002")
    response = model.predict(
        "Summarize this paragraph, Committee on Rules, Full Committee, hearing on H.R. 7160, the ""SALT Marriage Penalty Elimination Act”; and H. Res. 987, denouncing the harmful, anti-American en- ergy policies of the Biden administration, and for other purposes, 8 a.m., H-313 Capitol.",
        **parameters,
    )
    print(f"Response from Model: {response.text}")
interview()
print("")
print("")
