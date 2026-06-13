import json
import streamlit as st

with open("storage/metadata/nrc_data.json") as f:
    nrc = json.load(f)

st.metric("NRC Documents", len(nrc))
