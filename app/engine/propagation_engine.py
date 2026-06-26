import networkx as nx
import pandas as pd


class ImpactPropagationEngine:

    def __init__(self, rkg_df):

        self.rkg_df = rkg_df

        self.G = nx.DiGraph()

        self._build_graph()


    def _build_graph(self):

        for _, r in self.rkg_df.iterrows():

            if pd.notna(r.get("change_id")) and pd.notna(r.get("affected_requirement")):
                self.G.add_edge(
                    r["change_id"],
                    r["affected_requirement"]
                )

            if pd.notna(r.get("affected_requirement")) and pd.notna(r.get("affected_verification")):
                self.G.add_edge(
                    r["affected_requirement"],
                    r["affected_verification"]
                )

            if pd.notna(r.get("affected_verification")) and pd.notna(r.get("affected_test")):
                self.G.add_edge(
                    r["affected_verification"],
                    r["affected_test"]
                )

            if pd.notna(r.get("affected_test")) and pd.notna(r.get("failure_id")):
                self.G.add_edge(
                    r["affected_test"],
                    r["failure_id"]
                )
