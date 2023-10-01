import pandas as pd
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

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

tokenizer = AutoTokenizer.from_pretrained("asafaya/bert-base-arabic")

model = AutoModel.from_pretrained("asafaya/bert-base-arabic")

input_word = 'كلاب'

arabic_database = solo_words

similarities = {}
input_embeddings = model(**tokenizer(input_word, return_tensors="pt"))["last_hidden_state"].squeeze(0)

failed = []
for word in arabic_database:
    word_embeddings = model(**tokenizer(word, return_tensors="pt"))["last_hidden_state"].squeeze(0)
    try:
        similarity_score = torch.nn.functional.cosine_similarity(input_embeddings, word_embeddings)
    except:
        failed.append(word)
        continue
    similarities[word] = similarity_score.mean().item()

print("failed for: " , len(failed))

sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

for word, score in sorted_similarities[:10]:
    print(word, score)

