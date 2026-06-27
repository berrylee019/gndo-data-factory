import networkx as nx
import pandas as pd

class GraphBuilder:

    @staticmethod
    def build(rkg_df):

        G = nx.DiGraph()

        edge_count = 0

        for _, r in rkg_df.iterrows():

            change = r.get("change_id")
            req = r.get("affected_requirement")
            ver = r.get("affected_verification")
            test = r.get("affected_test")
            fail = r.get("failure_id")

            if pd.notna(change) and pd.notna(req):
                G.add_edge(change, req)
                edge_count += 1

            if pd.notna(req) and pd.notna(ver):
                G.add_edge(req, ver)
                edge_count += 1

            if pd.notna(ver) and pd.notna(test):
                G.add_edge(ver, test)
                edge_count += 1

            if pd.notna(test) and pd.notna(fail):
                G.add_edge(test, fail)
                edge_count += 1

        print("EDGE COUNT =", edge_count)
        print("GRAPH NODES =", len(G.nodes()))
        print("GRAPH EDGES =", len(G.edges()))

        return G
