from flask import Flask, request
import pandas as pd
from  Mazajak.finder import get_match

app = Flask(__name__)

excel_file = "data/output-excel.csv"
df = pd.read_csv(excel_file)

multi_words = []
solo_words = []

for index, row in df.iterrows():
    word = str(row[0])
    if len(word.split(" ")) > 1:
        multi_words.append(word)
    else:
        solo_words.append(word)

@app.route("/get-match", methods=["POST"])
def route_get_match():
    word = request.form['word']
    return {"data" : get_match(word, solo_words)}

if __name__ == "__main__":
    app.run()