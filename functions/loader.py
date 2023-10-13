import pandas as pd

def load_files():
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
    
    return multi_words, solo_words, letters