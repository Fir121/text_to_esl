import pandas as pd
import Arabycia.Arabycia as Arabycia

excel_file = "data/output-excel.csv"
df = pd.read_csv(excel_file)

multi_words = []
solo_words = []
letters = []

for index, row in df.iterrows():
    word = str(row[0])
    if len(word.split(" ")) > 1:
        multi_words.append(word)
    elif len(word) == 1:
        letters.append(word)
    else:
        solo_words.append(word)

word = "يكتب"
text = " ".join(solo_words)
arabycia = Arabycia.Arabycia()
arabycia.set_raw_text(text)
search_result = arabycia.text_search(arabycia.stem(word))
print(search_result)

if word in solo_words:
    print(True)
