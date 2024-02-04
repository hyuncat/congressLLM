# https://pypi.org/project/semantic-text-similarity/

from semantic_text_similarity.models import WebBertSimilarity
from semantic_text_similarity.models import ClinicalBertSimilarity

web_model = WebBertSimilarity(device='cpu', batch_size=10) #defaults to GPU prediction

clinical_model = ClinicalBertSimilarity(device='cuda', batch_size=10) #defaults to GPU prediction

# irrel = "/Arts & Entertainment/Events & Listings/Food & Beverage Events"
# rel = "/Health/Public Health/Toxic Substances & Poisoning"

# test1 = "health"
# test2 = "finance"
# test3 = "jobs and education"



# print(web_model.predict([(irrel, test1)]))
# print(web_model.predict([(rel, test1)]))
# print(web_model.predict([(rel, test2)]))

in_key_fp = "keywords.txt"

# Open the file in read mode
with open(in_key_fp, 'r') as file:
    # Read lines and store them in a list
    bigcats = file.readlines()    

in_v2_fp = "v2.txt"
with open(in_v2_fp, "r") as file:
    smallcats = file.readlines()

# df = pd.DataFrame {
#     'big_cat':
#     'small_cat':
# }
    
out_fp = "categoryreduction.csv"

for scat in smallcats:
    print(scat)
    largest_n = 0
    most_similar_cat = ""
    for bcat in bigcats:
        n = web_model.predict([(scat, bcat)])
        n_as_float = float(n[0])
        if n_as_float > largest_n:
            largest_n = n_as_float
            most_similar_cat = bcat

    with open(out_fp, 'a') as file:
        file.write(scat.strip() + "," + most_similar_cat)

    print(largest_n, most_similar_cat)



# largest = 0

# for l in lines:
#     n = (l, web_model.predict([(test, l)]))
#     print(n)
#     # if n > largest:
#     #     largest = n

# print("largest", largest)



