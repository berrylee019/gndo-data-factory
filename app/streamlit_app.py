############################################################
# GNDO Data Factory v1.3
# Streamlit Main App
############################################################
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
    
import streamlit as st
import pandas as pd
import networkx as nx

from pyvis.network import Network

import streamlit.components.v1 as components

import tempfile
from pathlib import Path

############################################################
# GNDO Engine
############################################################

from gndo_engine.graph_builder_v3 import GraphBuilderV3
from gndo_engine.graph_visualizer import GraphVisualizer
from gndo_engine.traceability_engine import TraceabilityEngine
from gndo_engine.impact_engine import ImpactEngine

############################################################
# Agents
############################################################

#from agents.nureg_agent import NuregAgent
#from agents.rg_agent import RGAgent
#from agents.srp_agent import SRPAgent
#from agents.cfr_agent import CFRAgent
#from agents.ap1000_agent import AP1000Agent
#from agents.apr1400_agent import APR1400Agent
#from agents.crosswalk_agent import CrosswalkAgent
#from agents.rkg_agent import RegulatoryKnowledgeGraphAgent

############################################################
# Utility
############################################################

import warnings

warnings.filterwarnings("ignore")

