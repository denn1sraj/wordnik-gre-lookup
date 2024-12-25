import pandas as pd
import json
from urllib.request import urlopen
from time import sleep

# read in the API key
with open("Key/wordnikapi.txt", "r") as file:
    key = file.read()

# wordnik base url
base_url = 'https://api.wordnik.com/v4/word.json/'

# import GRE words
df = pd.read_csv("Assets/gre words.csv")

# add the new columns to the dataframe
df = df.assign(part='', 
               definition = '',
               synonyms = '',
               example = '')

# testing limit 
limit = 1

for row in df.itertuples():
    # testing 
    # if row.Index > limit:
    #     break
    print(f"Index: {row.Index}, Word: {row.Word}")
    url_def = f"{base_url}{row.Word}/definitions?api_key={key}"
    url_rel = f"{base_url}{row.Word}/relatedWords?api_key={key}"
    url_topex = f"{base_url}{row.Word}/topExample?api_key={key}"

    # call / store json for definition
    response = urlopen(url_def)
    json_data = json.loads(response.read())[0] ## pulls just the first response
    # extract definition data
    definition = json_data['text']
    part = json_data['partOfSpeech']

    # repeat call / store for synonym
    response = urlopen(url_rel)
    json_data = json.loads(response.read())
    # extract synonym data
    synonyms = next(item['words'] for item in json_data if item['relationshipType'] == 'synonym')

    # repeat call / store for top example
    response = urlopen(url_topex)
    json_data = json.loads(response.read())
    # extract example data
    example = json_data['text']

    print(f"Updating: {row.Word}")
    df.at[row.Index, 'part'] = part
    df.at[row.Index, 'definition'] = definition
    df.at[row.Index, 'synonyms'] = synonyms
    df.at[row.Index, 'example'] = example
    print(f"{row.Word} is updated with the part of speech, definition, synonyms and examples")



    headers = response.info()
    rate_remaining = headers.get("X-RateLimit-Remaining-Minute")
    print("Rate Remaining (Per Minute):", rate_remaining)
    sleep(30)

file_path = "Output/gre words updated.csv"

df.to_csv(file_path, index=False)
print(f"File '{file_path}' written successfully!")

    

    




    

