import pandas as pd
import Arabycia.Arabycia as Arabycia

def check_for_stem(word, check_list):
    text = " ".join(check_list)
    arabycia = Arabycia.Arabycia()
    arabycia.set_raw_text(text)
    search_result = arabycia.text_search(arabycia.stem(word))
    if search_result and len(search_result) == 1:
        return search_result[0]
    return None
