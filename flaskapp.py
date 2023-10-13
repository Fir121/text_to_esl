from flask import Flask, request
from  Mazajak.finder import get_match
from functions.loader import load_files

app = Flask(__name__)

multi_words, solo_words, letters = load_files()

@app.route("/get-match", methods=["POST"])
def route_get_match():
    word = request.form['word']
    return {"data" : get_match(word, solo_words)}

if __name__ == "__main__":
    app.run()