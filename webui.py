import os
from typing import List, Union

import requests
import streamlit as st

from annotated_text import annotated_text
import json

import aisa


def load_prompts() -> List[Union[str, os.PathLike]]:
    prompts = []

    if os.path.exists("prompts"):
        prompt_dir = "prompts"
        for root, dirs, files in os.walk(prompt_dir):
            for file in files:
                if file.endswith(".prompt"):
                    prompts.append(os.path.join(root, file))

    return sorted(prompts)


def read_prompt_file(prompt_file_path: Union[str, os.PathLike]) -> str:
    with open(prompt_file_path) as prompt_file:
        prompt = prompt_file.read()

    return prompt


if "result" not in st.session_state:
    st.session_state.result = ""

if "prompt_files" not in st.session_state:
    st.session_state.prompt_files = load_prompts()

if "selected_prompt_file" not in st.session_state:
    st.session_state.selected_prompt_file = st.session_state.prompt_files[0]

if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = read_prompt_file(
        st.session_state.selected_prompt_file
    )


def update_prompts(prompt_file):
    prompt = read_prompt_file(prompt_file)
    st.session_state.current_prompt = prompt 

def post_annot():
    print("calling post_annot")
    resp = requests.post(
        "http://localhost:8000/annot",
        json={
            "text": input_text,
            "prompt": input_prompt,
        },
    )

    if resp.status_code == 200:
        print(resp.json())
        result = resp.json()
        result = [tuple(x) if type(x) is list else x for x in result]
        st.session_state.result = result


st.set_page_config(page_title="AISA", layout="wide")

with st.sidebar:
    st.write("AISA ver. {}".format(aisa.__version__))

    st.file_uploader(label="Szöveg feltöltése")

    selected_prompt_file = st.selectbox(
        label="Beépített promptok",
        options=st.session_state.prompt_files,
    )

    st.session_state.selected_prompt_file = selected_prompt_file 
    update_prompts(st.session_state.selected_prompt_file)

    st.button("Annotálás", on_click=post_annot)

col1, col2 = st.columns(2)

with col1:
    input_text = st.text_area(label="Szöveg", height=390)


with col2:
    input_prompt = st.text_area(
        label="Prompt", height=390, value=st.session_state.current_prompt
    )

#try:
#    json.loads(st.session_state.result)
#    st.json(st.session_state.result)
#except:
#    st.write(st.session_state.result)

annotated_text(st.session_state.result)
