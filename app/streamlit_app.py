import streamlit as st
import json

st.title("GNDO Data Factory")

def load_data(path):

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    except:
        return []

nrc = load_data(
    "storage/metadata/nrc_data.json"
)

ap1000 = load_data(
    "storage/metadata/ap1000_data.json"
)

apr1400 = load_data(
    "storage/metadata/apr1400_data.json"
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "NRC Documents",
    len(nrc)
)

col2.metric(
    "AP1000 Documents",
    len(ap1000)
)

col3.metric(
    "APR1400 Documents",
    len(apr1400)
)

st.subheader("Latest NRC Data")
st.json(nrc)

st.subheader("Latest AP1000 Data")
st.json(ap1000)

st.subheader("Latest APR1400 Data")
st.json(apr1400)
