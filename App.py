import openai
import streamlit as st
import pandas as pd
from  Mazajak.finder import get_match
from Grammar.processor import fix_grammar
from contplayer.player import play_files, save_files, play_files_with_mediapipe
from audiorecorder import audiorecorder
import whisper
import os

openai.api_key = "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"

st.set_page_config(layout="wide", 
                   page_title="ESL",
                   page_icon="🎧",
                   initial_sidebar_state="collapsed")

#Can cache these as cache data as well  
excel_file = "data/output-excel.csv"
df = pd.read_csv(excel_file)
letters_excel_file = "data/output-letters.csv"
ldf = pd.read_csv(letters_excel_file)

def get_link_from_key(key, df):
    return key

def get_fingerspell_links(word):
    arr = []
    for letter in word:
        arr.append(get_link_from_key(letter, ldf))
    return arr

def processing(inp):
    inp = inp.strip()
    inp = inp.lower()
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

    inp = fix_grammar(inp)

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

    st.session_state['final_array'] = ans
    print(ans)
    return ans
    
def save_video(ans):
    for i in range(len(ans)):
        ans[i] += ".mp4"
    # play_files(ans)
    save_files(ans)
    st.session_state['file_saved'] = True

def audio_to_text():
    with open("audio.wav", "rb") as audio_file:
        transcript_ar = openai.Audio.transcribe(
            file = audio_file,
            model = "whisper-1",
            response_format="text",
            language="ar"
        )
    st.session_state['input_text'] = transcript_ar

def app():
    st.markdown("<h2 style='text-align: center;'>Arabic to Emirati Sign Language Translator</h2>", unsafe_allow_html=True)
    st.markdown("#")
    col1, col2 = st.columns([2, 1])
    with col1:
        tab1, tab2, tab3 = st.tabs(["Text", "Audio", "Video"])
        with tab1:
            st.session_state['input_text'] = st.text_area('Input text in arabic')

            if st.button("Submit Text"):
                ans = processing(st.session_state['input_text'])
                save_video(ans)     
                st.experimental_rerun()

            if len(st.session_state['final_array']) > 0:
                st.divider()
                st.text("Processed Text:")
                st.caption('   '.join(st.session_state['final_array']).replace(".mp4",""))  

        with tab2:
            st.text("Audio Recorder")
            audio = audiorecorder("Click to record", "Click to stop recording")

            if len(audio) > 0:
                # To play audio in frontend:
                st.audio(audio.export().read())  

                # To save audio to a file, use pydub export method:
                audio.export("audio.wav", format="wav")

            if st.button("Submit Audio"):
                audio_to_text()
                ans = processing(st.session_state['input_text'])
                save_video(ans)     
                st.experimental_rerun()

            if len(st.session_state['final_array']) > 0:
                st.divider()
                st.text("Processed Text:")
                st.caption('   '.join(st.session_state['final_array']).replace(".mp4",""))      

        with tab3:
            st.text("Add video part here")          
    
    with col2:
        st.markdown("#")
        if st.session_state['file_saved'] == True:
            st.text("Generated Sign Video:")
            video_file = open('final.mp4', 'rb')
            video_bytes = video_file.read()
            st.video(video_bytes)
        else:
            st.caption("We can add an image here")


# Run the Streamlit app
if __name__ == '__main__':
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

    if 'input_text' not in st.session_state:
        st.session_state['input_text'] = ""

    if 'final_array' not in st.session_state:
        st.session_state['final_array'] = []  

    if 'file_saved' not in st.session_state:
        st.session_state['file_saved'] = False
    
    app()
