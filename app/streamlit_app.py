############################################################
# GNDO Data Factory v1.3
############################################################

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import streamlit.components.v1 as components

import pandas as pd
import networkx as nx

from gndo_engine.graph_builder_v3 import GraphBuilderV3
from gndo_engine.graph_visualizer import GraphVisualizer
from gndo_engine.traceability_engine import TraceabilityEngine
from gndo_engine.impact_engine import ImpactEngine

############################################################
# Page
############################################################

st.set_page_config(
    page_title="GNDO Data Factory",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 GNDO Data Factory v1.3")
st.caption("Regulatory Knowledge Graph Explorer")

############################################################
# Load Data
############################################################

@st.cache_data
def load_documents():

    docs = pd.read_csv("data/documents.csv")

    return docs


@st.cache_data
def load_rkg():

    rkg = pd.read_csv("data/rkg.csv")

    return rkg


df = load_documents()

rkg_df = load_rkg()

############################################################
# Build Graph
############################################################

G = GraphBuilderV3.build(rkg_df)

############################################################
# Sidebar
############################################################

with st.sidebar:

    st.header("GNDO Summary")

    st.metric(
        "Documents",
        len(df)
    )

    st.metric(
        "Requirements",
        rkg_df["requirement_id"].nunique()
    )

    st.metric(
        "Graph Nodes",
        G.number_of_nodes()
    )

    st.metric(
        "Graph Edges",
        G.number_of_edges()
    )

############################################################
# Tabs
############################################################

dashboard_tab, crosswalk_tab, search_tab, graph_tab, trace_tab = st.tabs(
    [
        "📊 Dashboard",
        "🔗 Crosswalk",
        "📚 Document Search",
        "🌐 Knowledge Graph",
        "🧠 Traceability Explorer"
    ]
)
