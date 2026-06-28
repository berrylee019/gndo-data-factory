import networkx as nx
import pandas as pd


class GraphBuilder:

    @staticmethod
    def build(rkg_df):
        print("=== BUILD START ===")
        print("========== GRAPH BUILDER V2 ==========")
        print("Rows =", len(rkg_df))
        
        G = nx.DiGraph()
    
        for i, (_, r) in enumerate(rkg_df.iterrows()):
    
            if i < 5:
                print(
                    r["requirement_id"],
                    r["verification_id"],
                    r["test_id"],
                    r["failure_id"],
                    r["change_id"]
                )
            ##################################################
            # IDs
            ##################################################

            req = r.get("requirement_id")
            ver = r.get("verification_id")
            test = r.get("test_id")
            fail = r.get("failure_id")

            change = r.get("change_id")

            affected_req = r.get("affected_requirement")
            affected_ver = r.get("affected_verification")
            affected_test = r.get("affected_test")

            ##################################################
            # Requirement
            ##################################################

            if pd.notna(req):

                G.add_node(
                    req,
                    type="REQ",
                    chapter=r.get("chapter"),
                    system=r.get("system_id"),
                    component=r.get("component_id")
                )

            ##################################################
            # Verification
            ##################################################

            if pd.notna(ver):

                G.add_node(
                    ver,
                    type="VER"
                )

            ##################################################
            # Test
            ##################################################

            if pd.notna(test):

                G.add_node(
                    test,
                    type="TEST"
                )

            ##################################################
            # Failure
            ##################################################

            if pd.notna(fail):

                G.add_node(
                    fail,
                    type="FAIL"
                )

            ##################################################
            # Change
            ##################################################

            if pd.notna(change):

                G.add_node(
                    change,
                    type="CHANGE"
                )

            ##################################################
            # Traceability
            ##################################################

            if pd.notna(req) and pd.notna(ver):

                G.add_edge(req, ver)

            if pd.notna(ver) and pd.notna(test):

                G.add_edge(ver, test)

            if pd.notna(test) and pd.notna(fail):

                G.add_edge(test, fail)

            ##################################################
            # Requirement -> Failure
            ##################################################

            if pd.notna(req) and pd.notna(fail):

                G.add_edge(req, fail)

            ##################################################
            # Change Impact
            ##################################################

            if pd.notna(change) and pd.notna(affected_req):

                G.add_edge(change, affected_req)

            if pd.notna(affected_req) and pd.notna(affected_ver):

                G.add_edge(affected_req, affected_ver)

            if pd.notna(affected_ver) and pd.notna(affected_test):

                G.add_edge(affected_ver, affected_test)

        print("Nodes =", G.number_of_nodes())
        print("Edges =", G.number_of_edges())
        
        print("=== BUILD END ===")
        return G, rkg_df.head()
