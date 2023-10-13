import gensim
import pandas as pd
from operator import itemgetter

embeddings = gensim.models.KeyedVectors.load_word2vec_format('Mazajak/data/sg_250.bin',binary=True,unicode_errors='ignore')

def get_match(word, word_list, threshold=0.45):
    d_arr = {}
    for w in word_list:
        try:
            d_arr[w] = embeddings.similarity(word, w) # can this be normalised, relative_cosine_similarity works but is very slow, need better solution for threshold
        except Exception as e:
            print(e)
            pass
    val = sorted(d_arr.items(), key=itemgetter(1), reverse=True)[:5]
    if len(val) == 0:
        return None
    val = val[0]
    if val[1] >= threshold:
        return val[0]
    return None

"""
excel_file = "data/output-excel.csv"
df = pd.read_csv(excel_file)
letters_excel_file = "data/output-letters.csv"
ldf = pd.read_csv(letters_excel_file)

multi_words = []
solo_words = []
letters = []

for index, row in df.iterrows():
    word = str(row[0])
    if len(word.split(" ")) > 1:
        multi_words.append(word)
    else:
        solo_words.append(word)

for index, row in ldf.iterrows():
    word = str(row[0])
    letters.append(word)
    
print(get_match("أقود", solo_words))
"""