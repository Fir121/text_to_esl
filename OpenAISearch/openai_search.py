from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
from ast import literal_eval
import numpy as np
from openai.embeddings_utils import get_embedding
import openai
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

openai.api_key = os.getenv("OPENAI_KEY")

def search_reviews(df, product_description, n=3, pprint=True):
    product_embedding = get_embedding(
        product_description,
        engine="text-embedding-ada-002"
    )
    df["similarity"] = df.embedding.apply(lambda x: cosine_similarity(x, product_embedding))

    results = (
        df.sort_values("similarity", ascending=False)
        .head(n)
    )
    if pprint:
        print(results)
    return results


excel_file = "data/output-excel-embeds.csv"  # Replace with the path to your Excel file
df = pd.read_csv(excel_file)

df["embedding"] = df.embedding.apply(literal_eval).apply(np.array)

res = search_reviews(df, 'مركبة', n=3)