import streamlit as st
import json
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="GNDO Data Factory",
    layout="wide"
)

st.title("☢️ GNDO Document Explorer")

def load_json(path):

    if not Path(path).exists():
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
nureg = load_json(
    "storage/metadata/nureg_data.json"
)

rg = load_json(
    "storage/metadata/rg_data.json"
)

srp = load_json(
    "storage/metadata/srp_data.json"
)

cfr = load_json(
    "storage/metadata/cfr_data.json"
)

ap1000 = load_json(
    "storage/metadata/ap1000_data.json"
)

nrc = nureg + rg + srp + cfr
all_docs = nrc
df = pd.DataFrame(all_docs)

if df.empty:
    st.warning("No documents found.")
    st.stop()
c1, c2, c3 = st.columns(3)

c1.metric(
    "NRC",
    len(nrc)
)

st.subheader("Search")

search_term = st.text_input(
    "Search documents"
)
selected_sources = st.multiselect(
    "Source Filter",
    options=df["source"].unique(),
    default=df["source"].unique()
)
selected_categories = st.multiselect(
    "Category Filter",
    options=df["category"].unique(),
    default=df["category"].unique()
)
filtered_df = df[
    (df["source"].isin(selected_sources))
    &
    (df["category"].isin(selected_categories))
]

if search_term:

    filtered_df = filtered_df[
        filtered_df["title"]
        .str.contains(
            search_term,
            case=False,
            na=False
        )
    ]
st.subheader("Documents")

st.dataframe(
    filtered_df,
    use_container_width=True
)
for _, row in filtered_df.iterrows():

    with st.expander(row["title"]):

        st.write(
            f"Source: {row['source']}"
        )

        st.write(
            f"Category: {row.get('category','')}"
        )

        if row.get("url"):

            st.link_button(
                "Open Document",
                row["url"]
            )
