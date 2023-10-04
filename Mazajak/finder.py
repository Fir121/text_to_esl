import gensim
import pandas as pd
from operator import itemgetter

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

embeddings = gensim.models.KeyedVectors.load_word2vec_format('Mazajak/data/sg_250.bin',binary=True,unicode_errors='ignore')

d_arr = {}
inp = 'سيارات'
for word in solo_words:
    try:
        d_arr[word] = embeddings.similarity(inp, word)
    except:
        pass
print(sorted(d_arr.items(), key=itemgetter(1), reverse=True)[:5])
print(sorted(d_arr, key=d_arr.get, reverse=True)[:5])