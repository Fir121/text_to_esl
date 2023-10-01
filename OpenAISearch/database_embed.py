# imports
import pandas as pd
import tiktoken

from openai.embeddings_utils import get_embedding
import openai
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

openai.api_key = os.getenv("OPENAI_KEY")

# embedding model parameters
embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191

# load & inspect dataset
input_datapath = "data/output-excel.csv"  # to save space, we provide a pre-filtered dataset
df = pd.read_csv(input_datapath)
print(df.head(2))

encoding = tiktoken.get_encoding(embedding_encoding)
df["n_tokens"] = df["Words"].apply(lambda x: len(encoding.encode(x)))

df["embedding"] = df["Words"].apply(lambda x: get_embedding(x, engine=embedding_model))
df.to_csv("data/output-excel-embeds.csv")
