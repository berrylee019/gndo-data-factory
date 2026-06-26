from engine.graph_builder import GraphBuilder
from engine.semantic_expansion import SemanticExpansion

import networkx as nx


class ImpactPropagationEngine:

    def __init__(self, rkg_df):

        self.rkg_df = rkg_df

        self.G = GraphBuilder.build(rkg_df)
