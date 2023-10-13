import pandas as pd
# from ArabcyiaUsage.search import check_for_stem
from  Mazajak.finder import get_match
from Grammar.processor import fix_grammar
from contplayer.player import play_files, save_files, play_files_with_mediapipe
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import openai, os

openai.api_key = os.getenv("OPENAI_KEY")
# user input
inp = input("Enter Sentence: ")
inp = inp.strip()
inp = inp.lower()

# pandas fn
def get_link_from_key(key, df):
    return key

# Loads in all words, stores in arrays
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


# Grammar fix pipleline
inp = fix_grammar(inp)
print(inp)

# finger spell getter
def get_fingerspell_links(word):
    arr = []
    for letter in word:
        arr.append(get_link_from_key(letter, ldf))
    return arr

# Word Match Pipeline
print("Processing", inp)
# First check multi word
for i in range(len(multi_words)):
    if multi_words[i] in inp:
        inp.replace(multi_words[i], f"MREPL{i}")
# ['أناني', 'أ', 'ق', 'و', 'د', 'سيارة', 'إ', 'ل', 'ى', 'كلية']

final_arr = inp.split(" ")
for i in range(len(final_arr)):
    word = final_arr[i]
    if word.startswith("MREPL"):
        key = multi_words[int(word.lstrip("MREPL"))]
        final_arr[i] = get_link_from_key(key, df)
    # elif check_for_stem(word, solo_words) is not None:
    #     key = check_for_stem(word, solo_words)
    #     final_arr[i] = get_link_from_key(key, df)
    elif get_match(word, solo_words) is not None:
        key = get_match(word, solo_words)
        final_arr[i] = get_link_from_key(key, df)
    else:
        final_arr[i] = get_fingerspell_links(word)

ans = []
for x in final_arr:
    if type(x) == str:
        ans.append(x)
    else:
        for y in x:
            ans.append(y)

for i in range(len(ans)):
    ans[i] += ".mp4"

print(ans)
play_files(ans)
save_files(ans)
play_files_with_mediapipe(ans)


"""
ISSUES  - Need more words, common ones like me you him, stuff like grammar words. Maybe can take that from arabic sign language
        - Video Gen
"""