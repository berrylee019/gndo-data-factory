import networkx as nx
import pandas as pd


class GraphBuilder:

    @staticmethod
    def build(rkg_df):

        G = nx.DiGraph()

        for _, r in rkg_df.iterrows():

            if pd.notna(r.get("change_id")) and pd.notna(r.get("affected_requirement")):
                G.add_edge(
                    r["change_id"],
                    r["affected_requirement"]
                )

            if pd.notna(r.get("affected_requirement")) and pd.notna(r.get("affected_verification")):
                G.add_edge(
                    r["affected_requirement"],
                    r["affected_verification"]
                )

            if pd.notna(r.get("affected_verification")) and pd.notna(r.get("affected_test")):
                G.add_edge(
                    r["affected_verification"],
                    r["affected_test"]
                )

            if pd.notna(r.get("affected_test")) and pd.notna(r.get("failure_id")):
                G.add_edge(
                    r["affected_test"],
                    r["failure_id"]
                )

        return G
