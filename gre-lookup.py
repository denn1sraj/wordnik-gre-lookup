import pandas as pd
import json
from urllib.request import urlopen
from time import sleep

# read in the API key
with open("Key/wordnikapi.txt", "r") as file:
    key = file.read()

# wordnik base url
base_url = 'https://api.wordnik.com/v4/word.json/'

# define a log file
log_file = "error_log.txt"

# import GRE words
df = pd.read_csv("Assets/gre words.csv")

# add the new columns to the dataframe
df = df.assign(part='', 
               definition = '',
               synonyms = '',
               example = '')

# testing limit 
# limit = 30 // ucomment to add break

with open("error_log.txt", "w") as log:

    for row in df.itertuples():
        # testing // uncomment to add break
        # if row.Index > limit:
        #     break
        try: 

            print(f"Starting Index: {row.Index}")

             # call / store json for definition
            current_url = f"{base_url}{row.Word}/definitions?api_key={key}"
            response = urlopen(current_url)
            json_data = json.loads(response.read())[0] ## pulls just the first response

            # extract definition data
            definition = json_data['text']
            part = json_data['partOfSpeech']

            # call / store for synonym
            current_url = f"{base_url}{row.Word}/relatedWords?api_key={key}"
            response = urlopen(current_url)
            json_data = json.loads(response.read())

            # extract synonym data
            synonyms = next(item['words'] for item in json_data if item['relationshipType'] == 'synonym')

            # repeat call / store for top example
            current_url = f"{base_url}{row.Word}/topExample?api_key={key}"
            response = urlopen(current_url)
            json_data = json.loads(response.read())
            
            # extract example data
            example = json_data['text']
            
            print(f"Updating: {row.Word}")
            df.at[row.Index, 'part'] = part
            df.at[row.Index, 'definition'] = definition
            df.at[row.Index, 'synonyms'] = synonyms
            df.at[row.Index, 'example'] = example
            print(f"{row.Word} is updated with the part of speech, definition, synonyms and examples")
            print(f"Index {row.Index} processed correctly")
        
        # check rate
            headers = response.info()
            rate_remaining = int(headers.get("X-RateLimit-Remaining-Minute", 1))
            print("Rate Remaining (Per Minute):", rate_remaining, "\n")
            if rate_remaining < 3:
                print("Approaching rate limit. Sleeping for 45 seconds. \n")
                sleep(45)
            else:
                sleep(5)

        except Exception as e:
                log.write(f"error processing row {row.Index} for URL {current_url} - {e}\n")
                print(f"Error processing row {row.Index} for {row.Word} \nWaiting 45 seconds before processing the next word. \n")
                sleep(45)

file_path = "Output/gre words updated.csv"

df.to_csv(file_path, index=False)
print(f"File '{file_path}' written successfully!")

    

    




    

