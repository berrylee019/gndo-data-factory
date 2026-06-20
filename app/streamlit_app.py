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

rkg = load_json(
    "storage/metadata/rkg_data_v10.json"
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

tab1, tab2, tab3, tab4, tab5 = st.tabs(
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

    c1, c2, c3, c4, c5 = st.columns(5)

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

    c5.metric(
        "RKG Links",
        len(rkg)
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

    search_tab, gndo_tab, ask_tab = st.tabs(
        [
            "📄 Document Search",
            "🔍 GNDO Search",
            "🤖 Ask GNDO"
        ]
    )

    with search_tab:

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

    with gndo_tab:
        
        st.subheader(
            "GNDO Search"
        )
        
        st.write(
            rkg_df.columns.tolist()
        )
        
        gndo_search = st.text_input(
            "Search GNDO Objects"
        )
    
    
        rkg_df = pd.DataFrame(rkg)
    
        gndo_result = pd.DataFrame()
    
        if gndo_search:
    
            gndo_result = rkg_df[
                rkg_df.astype(str)
                .apply(
                    lambda x:
                    x.str.contains(
                        gndo_search,
                        case=False,
                        na=False
                    )
                )
                .any(axis=1)
            ]
        
            st.success(
                f"{len(gndo_result)} records found"
            )
        
            st.dataframe(
                gndo_result[
                    [
                        "chapter",
                        "requirement_id",
                        "verification_id",
                        "test_id",
                        "artifact_id",
                        "failure_id",
                        "system_id",
                        "component_id"
                    ]
                ],
                use_container_width=True
            )
    
            for _, row in gndo_result.iterrows():
        
                with st.expander(
            
                    f"{row.get('chapter')} | "
                    f"{row.get('topic')}"
            
                ):
            
                    st.json(
                        row.to_dict()
                    )
            
        selected_chapter = st.selectbox(
            "Select Chapter",
            sorted(
                [x["chapter"] for x in rkg]
            )
        )

    with ask_tab:
    
        st.subheader(
            "Ask GNDO"
        )
        
        ask_gndo = st.text_input(
            "Ask a Traceability Question"
        )
    
        if ask_gndo:
        
            result = rkg_df[
                rkg_df.astype(str)
                .apply(
                    lambda x:
                    x.str.contains(
                        ask_gndo,
                        case=False,
                        na=False
                    )
                )
                .any(axis=1)
            ]
    
            if result.empty:

                st.warning(
                    "No Traceability Found"
                )

            else:
                
                row = result.iloc[0]
        
                st.success(
                    "Traceability Path Found"
                )
        
                st.markdown(
                    f"""
    ### Requirement

    {row.get('requirement')}
    
    ### Traceability Chain
    
    {row.get('cfr')}
    
    ↓
    
    {row.get('rg')}
    
    ↓
    
    {row.get('nureg')}
    
    ↓
    
    {row.get('srp')}
    
    ↓
    
    {row.get('requirement_id')}
    
    ↓
    
    {row.get('verification_id')}
    
    ↓
    
    {row.get('test_id')}
    
    ↓
    
    {row.get('artifact_id')}
    
    ↓
    
    {row.get('system_id')}
    
    ↓
    
    {row.get('component_id')}
    """
                )

                with st.expander(
                    "Raw Record"
                ):
        
                    st.json(
                        row.to_dict()
                    )



with tab4:
    
    st.subheader(
        "🌐 GNDO Regulatory Knowledge Graph"
    )

    
    
    selected_chapter_graph = st.selectbox(
        "Knowledge Graph Chapter",
        ["ALL"] + sorted([x["chapter"] for x in rkg]),
        key="graph_chapter"
    )

    st.info(
        f"Current Chapter: {selected_chapter_graph}"
    )

    if selected_chapter_graph == "ALL":

        graph_data = rkg
    
    else:
    
        graph_data = [
            item
            for item in rkg
            if item["chapter"]
            == selected_chapter_graph
        ]


    c1, c2, c3, c4, c5, c6 = st.columns(6)

    c1.markdown("🔵 **IMPLEMENTED_BY**")
    c2.markdown("🟢 **GUIDES**")
    c3.markdown("🟣 **REVIEWED_BY**")
    c4.markdown("🟠 **APPLIED_TO**")
    c5.markdown("🔴 **EQUIVALENT_TO**")
    c6.markdown("🟡 **EXECUTED_BY**")

    st.divider()
    
    if rkg:

        G = nx.DiGraph()

        for item in graph_data:
        
            cfr = item["cfr"]
        
            rg = item["rg"]
        
            nureg = item["nureg"]
        
            srp = item["srp"]
    
            ap1000_node = item["ap1000"]
        
            apr1400_node = item["apr1400"]

            system_id = item.get(
                "system_id"
            )

            component_id = item.get(
                "component_id"
            )

            requirement_id = item.get(
                "requirement_id"
            )
        
            requirement_text = item.get(
                "requirement"
            )

            verification_id = item.get(
                "verification_id"
            )
            
            verification_name = item.get(
                "verification_name"
            )

            test_id = item.get(
                "test_id"
            )

            artifact_id = item.get(
                "artifact_id"
            )
            
            artifact_name = item.get(
                "artifact_name"
            )
            
            test_name = item.get(
                "test_name"
            )

            G.add_node(
                cfr,
                group="CFR",
                title=f"""
            CFR
            Chapter: {item['chapter']}
            Topic: {item['topic']}
            """
            )
                        
            G.add_node(
                nureg,
                group="NUREG",
                title=f"""
            NUREG
            Chapter: {item['chapter']}
            Topic: {item['topic']}
            """
            )
            
            G.add_node(
                rg,
                group="RG",
                title=f"""
            Regulatory Guide
            Chapter: {item['chapter']}
            Topic: {item['topic']}
            """
            )
            
            G.add_node(
                srp,
                group="SRP",
                title=f"""
            Standard Review Plan
            Chapter: {item['chapter']}
            Topic: {item['topic']}
            """
            )

            if requirement_id:
                
                G.add_node(
                    requirement_id,
                    group="REQUIREMENT",
                    title=f"""
            Requirement
            
            {requirement_text}
            """
                )

            if verification_id:

                G.add_node(
                    verification_id,
                    group="VERIFICATION",
                    title=f"""
            Verification
            
            {verification_name}
            """
                )

            if test_id:

                G.add_node(
                    test_id,
                    group="TEST",
                    title=f"""
            Test
            
            {test_name}
            """
                )

            if artifact_id:

                G.add_node(
                    artifact_id,
                    group="DOC",
                    title=f"""
            Design Artifact
            
            {artifact_name}
            """
                )

            if failure_id:

                G.add_node(
                    artifact_id,
                    group="FAILURE",
                    title=f"""
            Failure
            
            {artifact_name}
            """
                )
            if system_id:

                G.add_node(
                    system_id,
                    group="SYSTEM",
                    title=f"""
            System

            {item.get('system_name')}
            """
                )
            
            if component_id:
            
                G.add_node(
                    component_id,
                    group="COMPONENT",
                    title=f"""
            Component
            
            {item.get('component_name')}
            """
                )


            
            G.add_node(
                ap1000_node,
                group="AP1000",
                title=f"""
            AP1000
            Chapter: {item['chapter']}
            Topic: {item['topic']}
            """
            )
            
            G.add_node(
                apr1400_node,
                group="APR1400",
                title=f"""
            APR1400
            Chapter: {item['chapter']}
            Topic: {item['topic']}
            """
            )

            G.add_edge(
                cfr,
                rg,
                label="IMPLEMENTED_BY",
                color="#1f77b4"
            )
            
            G.add_edge(
                rg,
                nureg,
                label="GUIDES",
                color="#2ca02c"
            )
            
            G.add_edge(
                nureg,
                srp,
                label="REVIEWED_BY",
                color="#9467bd"
            )

            if requirement_id:

                G.add_edge(
                    srp,
                    requirement_id,
                    label="GENERATES",
                    color="#e377c2"
                )

            if requirement_id and failure_id:
            
                G.add_edge(
                    requirement_id,
                    failure_id,
                    label="CAUSES",
                    color="#ff4d4d"
                )
            
            if failure_id and verification_id:
            
                G.add_edge(
                    failure_id,
                    verification_id,
                    label="VERIFIED_BY",
                    color="#ff9999"
                )

            if requirement_id and verification_id:
            
                G.add_edge(
                    requirement_id,
                    verification_id,
                    label="VERIFIED_BY",
                    color="#bc5090"
                )

                G.add_edge(
                    failure_id,
                    verification_id,
                    label="VERIFIED_BY"
                )
            
            if verification_id and test_id:
            
                G.add_edge(
                    verification_id,
                    test_id,
                    label="EXECUTED_BY",
                    color="#ff7f0e"
                )

            if test_id and artifact_id:

                G.add_edge(
                    test_id,
                    artifact_id,
                    label="VALIDATES",
                    color="#bcbd22"
                )
    
            if test_id and system_id:
            
                G.add_edge(
                    test_id,
                    system_id,
                    label="VALIDATES",
                    color="#17becf"
                )

            if artifact_id and system_id:

                G.add_edge(
                    artifact_id,
                    system_id,
                    label="IMPLEMENTS",
                    color="#7f7f7f"
                )
    
            if system_id and component_id:

                G.add_edge(
                    system_id,
                    component_id,
                    label="CONTAINS",
                    color="#8c564b"
                )
            
            G.add_edge(
                srp,
                ap1000_node,
                label="APPLIED_TO",
                color="#ff7f0e"
            )
            
            G.add_edge(
                ap1000_node,
                apr1400_node,
                label="EQUIVALENT_TO",
                color="#d62728"
            )
            


        c1, c2 = st.columns(2)
        
        c1.metric(
            "Visible Nodes",
            len(G.nodes)
        )
        
        c2.metric(
            "Visible Relationships",
            len(G.edges)
        )
    
        net = Network(
            height="800px",
            width="100%",
            bgcolor="#ffffff",
            font_color="black"
        )

        net.from_nx(G)

        for edge in net.edges:
        
            edge["font"] = {
                "size": 14,
                "align": "middle"
            }
        
            edge["width"] = 3
        
            edge["arrows"] = "to"
        
            edge["smooth"] = {
                "type": "dynamic"
            }
    
        for node in net.nodes:
        
            if node["id"].startswith("CFR"):
                node["size"] = 40
        
            elif node["id"].startswith("RG"):
                node["size"] = 35
        
            elif node["id"].startswith("NUREG"):
                node["size"] = 30
        
            elif node["id"].startswith("SRP"):
                node["size"] = 25

            elif node["group"] == "REQUIREMENT":

                node["color"] = "#e377c2"
                node["size"] = 28

            elif node["group"] == "VERIFICATION":

                node["color"] = "#bc5090"
                node["size"] = 26

            elif node["group"] == "TEST":

                node["color"] = "#ff7f0e"
                node["size"] = 24
                
            elif node["group"] == "SYSTEM":
                node["size"] = 22
                node["color"] = "#17becf"
                
            elif node["group"] == "DOC":
                node["size"] = 24
                node["color"] = "#bcbd22"
    
            elif node["group"] == "COMPONENT":
                node["size"] = 18
                node["color"] = "#8c564b"

            elif node["id"].startswith("AP1000"):
                node["size"] = 20
                node["color"] = "#ffbf00"
        
            elif node["id"].startswith("APR1400"):
                node["size"] = 20
                node["color"] = "#d62728"

        for edge in net.edges:

            edge["font"] = {
                "size": 12
            }
            
        net.repulsion(
            node_distance=350,
            central_gravity=0.15,
            spring_length=350,
            spring_strength=0.02
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

    if not rkg:

        st.warning(
            "No RKG data found."
        )

    else:

        chapter_list = [
            item["chapter"]
            for item in rkg
        ]

        selected_chapter_trace = st.selectbox(
            "Traceability Chapter",
            chapter_list,
            key="trace_chapter"
        )

        selected = next(
            (
                item
                for item in rkg
                if item["chapter"]
                == selected_chapter_trace
            ),
            None
        )

        if selected:

            st.success(
                f"Chapter {selected['chapter']} : "
                f"{selected['topic']}"
            )

            st.code(
                f"""
        {selected['srp']}
            ↓
        {selected['ap1000']}
            ↓
        {selected['apr1400']}
        """,
                language="text"
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
