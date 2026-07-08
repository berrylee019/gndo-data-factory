import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
import streamlit as st
import json
import pandas as pd
from pathlib import Path
import streamlit as st
import json
import pandas as pd
from pathlib import Path
from gndo_engine.graph_builder_v3 import GraphBuilderV3
from gndo_engine.graph_visualizer import GraphVisualizer
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile

if "selected_node" not in st.session_state:
    st.session_state.selected_node = None

st.set_page_config(
    page_title="GNDO Data Factory",
    layout="wide"
)

def analyze_failure_impact(
    failure_id,
    rkg_df
):

    result = rkg_df[
        rkg_df["failure_id"] == failure_id
    ]

    if result.empty:
        return None

    row = result.iloc[0]

    st.session_state["impact_path"] = [
        row.get("failure_id"),
        row.get("requirement_id"),
        row.get("verification_id"),
        row.get("test_id"),
        row.get("artifact_id"),
        row.get("system_id"),
        row.get("component_id")
    ]

    impact_level = row.get(
        "impact_level"
    )
   
    retest_required = row.get(
        "retest_required"
    )
   
    safety_significant = row.get(
        "safety_significant"
    )

    recommendations = []

    if retest_required:
   
        recommendations.append(
            f"Re-execute {row.get('test_id')}"
        )
   
    if row.get("artifact_id"):
   
        recommendations.append(
            f"Review {row.get('artifact_id')}"
        )
   
    if row.get("system_id"):
   
        recommendations.append(
            f"Verify {row.get('system_id')}"
        )
   
    if row.get("component_id"):
   
        recommendations.append(
            f"Inspect {row.get('component_id')}"
        )
   
    if safety_significant:
   
        recommendations.append(
            "Engineering Review Required"
        )

    return {

        "failure_id":
            row.get("failure_id"),

        "failure_mode":
            row.get("failure_mode"),

        "requirement_id":
            row.get("requirement_id"),

        "verification_id":
            row.get("verification_id"),

        "test_id":
            row.get("test_id"),

        "artifact_id":
            row.get("artifact_id"),

        "system_id":
            row.get("system_id"),

        "component_id":
            row.get("component_id"),

        "recommendations":
            recommendations
    }


           
st.title("☢️ GNDO Document Explorer")


def load_json(path):

    if not Path(path).exists():
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


nureg = load_json("storage/metadata/nureg_data.json")
rg = load_json("storage/metadata/rg_data.json")
srp = load_json("storage/metadata/srp_data.json")
cfr = load_json("storage/metadata/cfr_data.json")

ap1000 = load_json("storage/metadata/ap1000_data.json")
apr1400 = load_json("storage/metadata/apr1400_data.json")

crosswalk = load_json("storage/metadata/crosswalk_data.json")

# v13 사용
rkg = load_json("storage/metadata/rkg_data_v12.json")

nrc = nureg + rg + srp + cfr

all_docs = nrc + ap1000 + apr1400

df = pd.DataFrame(all_docs)

rkg_df = pd.DataFrame(rkg)


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
    rkg_df = pd.DataFrame(rkg)
   
    with search_tab:

        st.subheader("Search")

        search_term = st.text_input(
            "Search documents",
            placeholder="예: NUREG-0800 Chapter 7, Plant Protection System"
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
                filtered_df.astype(str)
                .apply(
                    lambda x:
                    x.str.contains(
                    search_term,
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
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
   

        # ===========================
        # v1.4 Impact Propagation Graph
        # ===========================
       
        G = nx.DiGraph()
               
       
    with gndo_tab:
   
        st.subheader(
            "GNDO Search"
        )
   
        gndo_search = st.text_input(
            "Search GNDO Objects",
            placeholder="예: REQ-CH07-001, VER-CH07-001, TEST-CH07-001"
        )
   
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
       
            display_cols = [
                "chapter",
                "requirement_id",
                "failure_id",
                "verification_id",
                "test_id",
                "artifact_id",
                "system_id",
                "component_id"
            ]
           
            display_cols = [
                c
                for c in display_cols
                if c in gndo_result.columns
            ]
           
            st.dataframe(
                gndo_result[display_cols],
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

        G = nx.DiGraph()
       
        for _, r in rkg_df.iterrows():
       
            change_id = r.get("change_id")
            req_id = r.get("affected_requirement")
            ver_id = r.get("affected_verification")
            test_id = r.get("affected_test")
            fail_id = r.get("failure_id")
       
            if pd.notna(change_id) and pd.notna(req_id):
       
                G.add_edge(
                    change_id,
                    req_id
                )
       
            if pd.notna(req_id) and pd.notna(ver_id):
       
                G.add_edge(
                    req_id,
                    ver_id
                )
       
            if pd.notna(ver_id) and pd.notna(test_id):
       
                G.add_edge(
                    ver_id,
                    test_id
                )
       
            if pd.notna(req_id) and pd.notna(fail_id):
       
                G.add_edge(
                    req_id,
                    fail_id
                )
               
        ask_gndo = st.text_input(
            "Ask GNDO Question",
            placeholder="예: FAIL-CH07-001의 영향은?"
        )
       
        if ask_gndo:
       
            import re
       
            query = ask_gndo.upper()
       
            req_match = re.search(
                r"(REQ-CH\d{2}-\d{3})",
                query
            )
       
            ver_match = re.search(
                r"(VER-CH\d{2}-\d{3})",
                query
            )
       
            test_match = re.search(
                r"(TEST-CH\d{2}-\d{3})",
                query
            )
       
            fail_match = re.search(
                r"(FAIL-CH\d{2}-\d{3})",
                query
            )

            chg_match = re.search(
                r"(CHG-CH\d{2}-\d{3})",
                query
            )
           
            target_id = None
       
            if req_match:
                target_id = req_match.group(1)
       
                result = rkg_df[
                    rkg_df["requirement_id"] == target_id
                ]
       
            elif ver_match:
                target_id = ver_match.group(1)
       
                result = rkg_df[
                    rkg_df["verification_id"] == target_id
                ]
       
            elif test_match:
                target_id = test_match.group(1)
       
                result = rkg_df[
                    rkg_df["test_id"] == target_id
                ]
       
            elif fail_match:
                target_id = fail_match.group(1)
       
                result = rkg_df[
                    rkg_df["failure_id"] == target_id
                ]

            elif chg_match:
                target_id = chg_match.group(1)
       
                result = rkg_df[
                    rkg_df["change_id"] == target_id
                ]
       
            else:
       
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

                st.write(result[
                    [
                        "change_id",
                        "requirement_id",
                        "verification_id",
                        "artifact_id"
                    ]
                ].head(20))
       
                row = result.iloc[0]

                affected_requirements = []
                affected_verifications = []
                affected_tests = []
                affected_failures = []

                change_row = row

                if change_row.get("change_id"):
               
                    affected_req = change_row.get(
                        "affected_requirement"
                    )
               
                    affected_rows = rkg_df[
                        rkg_df["requirement_id"]
                        == affected_req
                    ]
               
                    if not affected_rows.empty:
               
                        requirement_row = affected_rows.iloc[0]

                if (
                    target_id
                    and target_id.startswith("FAIL-")
                ):
                    st.subheader(
                        "Failure Impact Analysis"
                    )

                elif (
                    target_id
                    and target_id.startswith("CHG-")
                ):

                    impact_nodes = []
   
                    if target_id in G:
                       
                        impact_nodes = list(
                            nx.descendants(
                                G,
                                target_id
                            )
                        )

                        # ==========================
                        # Semantic Expansion
                        # Same System
                        # ==========================
                       
                        semantic_nodes = set()
                       
                        for node in impact_nodes:
                       
                            if not str(node).startswith("REQ-"):
                                continue
                       
                            req_rows = rkg_df[
                                rkg_df["requirement_id"] == node
                            ]
                       
                            if req_rows.empty:
                                continue
                       
                            system_id = req_rows.iloc[0].get("system_id")
                       
                            if pd.isna(system_id):
                                continue
                       
                            same_system = rkg_df[
                                rkg_df["system_id"] == system_id
                            ]
                       
                            semantic_nodes.update(
                                same_system["requirement_id"]
                                .dropna()
                                .tolist()
                            )

                        impact_nodes = list(
                            set(impact_nodes)
                            |
                            semantic_nodes
                        )
                       
                        expanded_nodes = set(impact_nodes)

                        for req in semantic_nodes:
                       
                            if req in G:
                       
                                expanded_nodes.update(
                                    nx.descendants(
                                        G,
                                        req
                                    )
                                )
                       
                        impact_nodes = list(expanded_nodes)

                        st.subheader("Semantic Expansion")

                        st.write("Impact Nodes")
                        st.write(impact_nodes)
                       
                        st.write("Affected Requirements")
                        st.write(affected_requirements)
                       
                        st.write("Affected Verifications")
                        st.write(affected_verifications)
                       
                        st.write("Affected Tests")
                        st.write(affected_tests)
                       
                        st.write("Affected Failures")
                        st.write(affected_failures)
                       
   
                        affected_requirements = [
                            n
                            for n in impact_nodes
                            if str(n).startswith("REQ-")
                        ]
                       
                        affected_verifications = [
                            n
                            for n in impact_nodes
                            if str(n).startswith("VER-")
                        ]
                       
                        affected_tests = [
                            n
                            for n in impact_nodes
                            if str(n).startswith("TEST-")
                        ]
                       
                        affected_failures = [
                            n
                            for n in impact_nodes
                            if str(n).startswith("FAIL-")
                        ]
                   
                        c1, c2, c3, c4 = st.columns(4)
                        
                        with c1:
                            st.metric("REQ", len(affected_requirements))
                        
                        with c2:
                            st.metric("VER", len(affected_verifications))
                        
                        with c3:
                            st.metric("TEST", len(affected_tests))
                        
                        with c4:
                            st.metric("FAIL", len(affected_failures))
       
                        change_id = row.get(
                            "change_id"
                        )
                   
                        req_id = row.get(
                            "affected_requirement"
                        )
                   
                        ver_id = row.get(
                            "affected_verification"
                        )
                   
                        test_id = row.get(
                            "affected_test"
                        )
       
                        failure_id = row.get(
                            "failure_id"
                        )

                        G = GraphBuilderV3.build_impact_graph(row)
                        
                        highlight = set(G.nodes())
                        
                        impact_net = GraphVisualizer.build_network(
                            G,
                            highlight_nodes=highlight
                        )
                        
                        left, right = st.columns([3,2])
                        
                        with left:
                        
                            impact_html = GraphVisualizer.save_html(
                                impact_net
                            )

                            st.subheader("Impact Graph")
                            
                            node_list = sorted(G.nodes())

                            selected_node = st.selectbox(
                            
                                "Select Node",
                            
                                node_list,
                            
                                key="impact_node"
                            
                            )
                            
                            components.html(
                                impact_html,
                                height=650
                            )
                        
                        with right:
                        
                            st.subheader("📄 Node Detail")
                        
                            if selected_node:
                        
                                attr = G.nodes[selected_node]
                        
                                st.markdown(f"### {selected_node}")
                        
                                st.markdown("---")
                                
                                st.markdown(f"## {selected_node}")
                                
                                st.caption(attr.get("type",""))
                                
                                sections = [
                                
                                    ("Chapter", attr.get("chapter")),
                                
                                    ("Topic", attr.get("topic")),
                                
                                    ("System", attr.get("system")),
                                
                                    ("Component", attr.get("component")),
                                
                                    ("Requirement", attr.get("requirement")),
                                
                                    ("Verification", attr.get("verification")),
                                
                                    ("Verification Method", attr.get("verification_method")),
                                
                                    ("Acceptance", attr.get("acceptance")),
                                
                                    ("Test", attr.get("test")),
                                
                                    ("Artifact", attr.get("artifact")),
                                
                                    ("Failure", attr.get("failure")),
                                
                                    ("Severity", attr.get("severity")),
                                
                                    ("Consequence", attr.get("consequence")),
                                
                                    ("Mitigation", attr.get("mitigation"))
                                
                                ]
                                
                                for title, value in sections:
                                
                                    if value not in [None, "", "nan"]:
                                
                                        st.markdown(f"### {title}")
                                
                                        st.info(value)

                    
                       
                elif (
                    target_id
                    and target_id.startswith("REQ-")
                ):
                    st.subheader(
                        "Requirement Impact Analysis"
                    )
   
                elif (
                    target_id
                    and target_id.startswith("VER-")
                ):
                    st.subheader(
                        "Verification Impact Analysis"
                    )
   
                elif (
                    target_id
                    and target_id.startswith("TEST-")
                ):
                    st.subheader(
                        "Test Impact Analysis"
                    )
               
               
                    impact_cols = [
                        "requirement_id",
                        "verification_id",
                        "test_id",
                        "artifact_id",
                        "system_id",
                        "component_id"
                    ]
               
                    impact_df = result[
                        [
                            c
                            for c in impact_cols
                            if c in result.columns
                        ]
                    ]
               
                    st.dataframe(
                        impact_df,
                        use_container_width=True
                    )

                impact_level = row.get(
                    "impact_level"
                )
               
                retest_required = row.get(
                    "retest_required"
                )
               
                safety_significant = row.get(
                    "safety_significant"
                )

                st.success(
                    f"Traceability Found"
                )

                if impact_level == "HIGH":
   
                    st.error(
                        "Impact Level : HIGH"
                    )
               
                elif impact_level == "MEDIUM":
               
                    st.warning(
                        "Impact Level : MEDIUM"
                    )
               
                elif impact_level == "LOW":
               
                    st.success(
                        "Impact Level : LOW"
                    )
   
                if safety_significant:
   
                    st.error(
                        "Safety Significant : YES"
                    )
               
                else:
               
                    st.success(
                        "Safety Significant : NO"
                    )

                if retest_required:
   
                    st.warning(
                        "Retest Required : YES"
                    )
               
                else:
               
                    st.success(
                        "Retest Required : NO"
                    )
                   
                recommendations = []

                if retest_required:
               
                    recommendations.append(
                        f"Re-execute {row.get('test_id')}"
                    )
               
                if row.get("artifact_id"):
               
                    recommendations.append(
                        f"Review {row.get('artifact_id')}"
                    )
               
                if row.get("system_id"):
               
                    recommendations.append(
                        f"Verify {row.get('system_id')}"
                    )
               
                if row.get("component_id"):
               
                    recommendations.append(
                        f"Inspect {row.get('component_id')}"
                    )
               
                if safety_significant:
               
                    recommendations.append(
                        "Engineering Review Required"
                    )
                if (
                    target_id
                    and target_id.startswith("FAIL-")
                ):
               
               
                        st.markdown(
                            f"""
                    ### Failure
                   
                    {row.get('failure_id')}
                   
                    {row.get('failure_mode')}
                   
                    ---
                   
                    ### Affected Requirement
                   
                    {row.get('requirement_id')}
                   
                    ---
                   
                    ### Verification
                   
                    {row.get('verification_id')}
                   
                    ---
                   
                    ### Test
                   
                    {row.get('test_id')}
                   
                    ---
                   
                    ### Design Artifact
                   
                    {row.get('artifact_id')}
                   
                    ---
                   
                    ### System
                   
                    {row.get('system_id')}
                   
                    ---
                   
                    ### Component
                   
                    {row.get('component_id')}
                    """
                        )

                if (
                    target_id
                    and target_id.startswith("CHG-")
                ):
                   
               
                    st.markdown(
                        f"""
                ### Change
               
                {row.get('change_id')}
               
                ### Change Type
               
                {row.get('change_type')}
               
                ### Impact Scope
               
                {row.get('impact_scope')}
               
                ### Requires Reverification
               
                {row.get('requires_reverification')}
               
                ### Requires Retest
               
                {row.get('requires_retest')}

                ### Affected Requirement

                {row.get('affected_requirement')}
               
                ### Affected Verification
               
                {row.get('affected_verification')}
               
                ### Affected Test
               
                {row.get('affected_test')}
                """
                )
                       
                if recommendations:

                    st.subheader(
                        "Recommended Actions"
                    )
               
                    for rec in recommendations:
               
                        st.info(rec)
       
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

        impact_path = st.session_state.get(
            "impact_path",
            []
        )
       
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

            failure_id = item.get(
                "failure_id"
            )
           
            failure_mode = item.get(
                "failure_mode"
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
               
                node_color = (
                    "#ff0000"
                    if requirement_id in impact_path
                    else "#97C2FC"
                )
               
                G.add_node(
                    requirement_id,
                    group="REQUIREMENT",
                    color=node_color
                )

            if verification_id:

                node_color = (
                    "#ff0000"
                    if verification_id in impact_path
                    else "#97C2FC"
                )

                G.add_node(
                    verification_id,
                    group="VERIFICATION",
                    color=node_color,
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
                    color=node_color,
                    title=f"""
            Design Artifact
           
            {artifact_name}
            """
                )

           
            if failure_id:
           
                node_color = (
                    "#ff0000"
                    if failure_id in impact_path
                    else "#97C2FC"
                )
           
                G.add_node(
                    failure_id,
                    group="FAILURE",
                    title=f"""
            Failure Mode
           
            {failure_mode}
            """,
                    color=node_color
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

                node_color = (
                    "#ff0000"
                    if component_id in impact_path
                    else "#97C2FC"
                )
           
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
           
            edge_color = "#cccccc"
           
            if failure_id and verification_id:
               
                edge_color = (
                    "#ff0000"
                    if (
                        failure_id in impact_path
                        and
                        verification_id in impact_path
                    )
                    else "#cccccc"
                )
                   
                G.add_edge(
                    failure_id,
                    verification_id,
                    label="VERIFIED_BY",
                    color=edge_color,
                    width=4
                )

            if requirement_id and verification_id:
           
                G.add_edge(
                    requirement_id,
                    verification_id,
                    label="VERIFIED_BY",
                    color="#bc5090"
                )


           
            if verification_id and test_id:
           
                G.add_edge(
                    verification_id,
                    test_id,
                    label="TESTED_BY",
                    color="#ff7f0e"
                )

            if test_id and artifact_id:

                G.add_edge(
                    test_id,
                    artifact_id,
                    label="DOCUMENTED_BY",
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
           
            print(
                "FAILURE:",
                failure_id,
                "VERIFICATION:",
                verification_id
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
