import streamlit as st
import openai
openai.api_key = st.secrets['OPENAI_KEY']

from functions.loader import load_files
from audiorecorder import audiorecorder
from Grammar.processor import fix_grammar
from contplayer.player import save_files
import requests
from PIL import Image


### GENERAL SETUP
def req_get_match(word):
    return requests.post("http://127.0.0.1:5000/get-match", data={"word":word}).json()["data"]

def get_fingerspell_links(word):
    arr = []
    for letter in word:
        arr.append(letter)
    return arr


### ESL SETUP
multi_words, solo_words, letters = load_files()

def processing(inp):
    inp = inp.strip()
    inp = inp.lower()

    # Step 1: Adjust grammar to ESL style
    inp = fix_grammar(inp, st.secrets['OPENAI_KEY'])

    # Step 2: a: Set signs for the sign video entries consisting of multiple words
    for i in range(len(multi_words)):
        if multi_words[i] in inp:
            inp = inp.replace(multi_words[i], f"MREPL{i}")

    # Step 2: b: Set sign video for each word, fingerspell as backup
    final_arr = inp.split(" ")
    for i in range(len(final_arr)):
        word = final_arr[i]
        if word.startswith("MREPL"):
            key = multi_words[int(word.lstrip("MREPL"))]
            final_arr[i] = key
        elif word in solo_words:
            final_arr[i] = word
        elif req_get_match(word) is not None:
            key = req_get_match(word)
            final_arr[i] = key
        else:
            final_arr[i] = get_fingerspell_links(word)

    # Step 2: c: Make the final sign word, video array
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
    st.session_state['file_name'] = save_files(ans)
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


### STREAMLIT SETUP
st.set_page_config(layout="wide", 
                   page_title="ESL",
                   page_icon="🎧",
                   initial_sidebar_state="collapsed")

def app():
    st.markdown("<h2 style='text-align: center;'>Arabic to Emirati Sign Language Translator</h2>", unsafe_allow_html=True)
    st.markdown("#")
    col1, col2 = st.columns([2, 1])
    with col1:
        tab1, tab2 = st.tabs(["Text", "Audio"])
        with tab1:
            st.session_state['input_text'] = st.text_area('Input text in arabic')

            if st.button("Submit Text"):
                with st.spinner('Processing Text...'):
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
                with st.spinner('Processing Text...'):
                    audio_to_text()
                    ans = processing(st.session_state['input_text'])
                    save_video(ans)
                st.experimental_rerun()

            if len(st.session_state['final_array']) > 0:
                st.divider()
                st.text("Processed Text:")
                st.caption('   '.join(st.session_state['final_array']).replace(".mp4",""))
    
    with col2:
        st.markdown("#")
        if st.session_state['file_saved'] == True:
            st.text("Generated Sign Video:")
            video_file = open(st.session_state['file_name'], 'rb')
            video_bytes = video_file.read()
            st.video(video_bytes)
        else:
            image = Image.open('./assets/logo.png')

            st.image(image, width = 400)


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
