import pandas as pd

# import GRE words
df = pd.read_csv("Assets/gre words.csv")

print(df)

limit = 3 #desired limit for looped function
count = 0
print (count)

for row in df.itertuples():

    if count >= limit:
        break
    print(f"Index: {row.Index}, Word: {row.Word}")
    count = count + 1
    print(count)

count = 0



    

