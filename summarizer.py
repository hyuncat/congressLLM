import torch                

from transformers import AutoTokenizer, AutoModelWithLMHead

tokenizer = AutoTokenizer.from_pretrained('t5-base')
model = AutoModelWithLMHead.from_pretrained('t5-base', return_dict=True)

text = "S. 644, to expand the take-home prescribing of methadone through pharmacies, with an amendment in the nature of a substitute. S. 1840, to amend the Public Health Service Act to reauthorize and improve the National Breast and Cervical Cancer Early Detection Program for fiscal years 2024 through 2028, with an amendment in the nature of a substitute. S. 3393, to reauthorize the SUPPORT for Patients and Communities Act, with an amendment in the nature of a substitute."

inputs = tokenizer.encode("summarize: " + text,
return_tensors='pt',
max_length=512,
truncation=True)

summary_ids = model.generate(inputs, max_length=150, min_length=80, length_penalty=5., num_beams=2)

summary = tokenizer.decode(summary_ids[0])

print()
print(text)
print()
print(summary)