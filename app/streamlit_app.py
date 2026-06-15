import streamlit as st
import json
import pandas as pd
from pathlib import Path
import streamlit as st
import json
import pandas as pd
from pathlib import Path

import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile

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

apr1400 = load_json(
    "storage/metadata/apr1400_data.json"
)

crosswalk = load_json(
    "storage/metadata/crosswalk_data.json"
)

nrc = nureg + rg + srp + cfr
all_docs = (
    nrc
    + ap1000
    + apr1400
)
df = pd.DataFrame(all_docs)

if df.empty:
    st.warning("No documents found.")
    st.stop()

tab1, tab2, tab3, tab4, tabs5 = st.tabs(
    [
        "📊 Dashboard",
        "🔗 Crosswalk",
        "📚 Documents",
        "🌐 Knowledge Graph",
        "🧠 Traceability Explorer"
    ]
)

with tab1:

    st.subheader("GNDO Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "NRC",
        len(nrc)
    )

    c2.metric(
        "AP1000",
        len(ap1000)
    )

    c3.metric(
        "APR1400",
        len(apr1400)
    )

    c4.metric(
        "Knowledge Links",
        len(crosswalk)
    )

    st.info(
        f"Total Knowledge Nodes: {len(nrc)+len(ap1000)+len(apr1400)}"
    )
    
with tab2:

    st.subheader(
        "Regulatory Knowledge Graph Crosswalk"
    )

    st.dataframe(
        pd.DataFrame(crosswalk),
        use_container_width=True
    )

with tab3:

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

    st.subheader(
        "Documents"
    )

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    for _, row in filtered_df.iterrows():

        with st.expander(
            row["title"]
        ):

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

with tab4:

    st.subheader(
        "🌐 GNDO Regulatory Knowledge Graph"
    )

    if crosswalk:

        G = nx.Graph()

        for item in crosswalk:

            srp = item["srp"]
            ap1000_node = item["ap1000"]
            apr1400_node = item["apr1400"]

            G.add_node(
                srp,
                group="SRP"
            )

            G.add_node(
                ap1000_node,
                group="AP1000"
            )

            G.add_node(
                apr1400_node,
                group="APR1400"
            )

            G.add_edge(
                srp,
                ap1000_node
            )

            G.add_edge(
                ap1000_node,
                apr1400_node
            )

        net = Network(
            height="800px",
            width="100%",
            bgcolor="#ffffff",
            font_color="black"
        )

        net.from_nx(G)

        net.repulsion(
            node_distance=200,
            central_gravity=0.3,
            spring_length=200,
            spring_strength=0.05
        )

        tmp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".html"
        )

        net.save_graph(
            tmp_file.name
        )

        with open(
            tmp_file.name,
            "r",
            encoding="utf-8"
        ) as f:

            html = f.read()

        components.html(
            html,
            height=850,
            scrolling=True
        )

    else:

        st.info(
            "No crosswalk data available."
        )

with tab5:

    st.subheader(
        "🧠 Regulatory Traceability Explorer"
    )

    if not crosswalk:

        st.warning(
            "No crosswalk data found."
        )

    else:

        chapter_list = [
            item["chapter"]
            for item in crosswalk
        ]

        selected_chapter = st.selectbox(
            "Select Chapter",
            chapter_list
        )

        selected = next(
            (
                item
                for item in crosswalk
                if item["chapter"]
                == selected_chapter
            ),
            None
        )

        if selected:

            st.success(
                f"Chapter {selected['chapter']} : "
                f"{selected['topic']}"
            )

            st.markdown(
                f"""
            ### Regulatory Mapping
            
            {selected['srp']}
            
            ⬇️
            
            {selected['ap1000']}
            
            ⬇️
            
            {selected['apr1400']}
            """
            )
            
        c1, c2, c3 = st.columns(3)

        c1.metric(
            "SRP",
            selected["srp"]
        )

        c2.metric(
            "AP1000",
            selected["ap1000"]
        )

        c3.metric(
            "APR1400",
            selected["apr1400"]
        )       
