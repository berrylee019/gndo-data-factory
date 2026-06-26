import json
import streamlit as st
from pathlib import Path

def load_json(path):

    if not Path(path).exists():
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

nrc = load_json(
    "storage/master/nrc_master.json"
)

st.metric(
    "NRC Documents",
    len(nrc)
)
