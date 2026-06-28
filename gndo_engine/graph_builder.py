def valid_id(x):
    return (
        isinstance(x, str)
        and x.strip() != ""
    )
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

            if valid_id(req):

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

            if valid_id(ver):

                G.add_node(
                    ver,
                    type="VER"
                )

            ##################################################
            # Test
            ##################################################

            if valid_id(test):

                G.add_node(
                    test,
                    type="TEST"
                )

            ##################################################
            # Failure
            ##################################################

            if valid_id(fail):

                G.add_node(
                    fail,
                    type="FAIL"
                )

            ##################################################
            # Change
            ##################################################

            if valid_id(change):

                G.add_node(
                    change,
                    type="CHANGE"
                )

            ##################################################
            # Traceability
            ##################################################

            if valid_id(req) and valid_id(ver):

                G.add_edge(req, ver)

            if valid_id(ver) and valid_id(test):

                G.add_edge(ver, test)

            if valid_id(test) and valid_id(fail):

                G.add_edge(test, fail)

            ##################################################
            # Requirement -> Failure
            ##################################################

            if valid_id(req) and valid_id(fail):

                G.add_edge(req, fail)

            ##################################################
            # Change Impact
            ##################################################

            if valid_id(change) and valid_id(affected_req):

                G.add_edge(change, affected_req)

            if valid_id(affected_req) and valid_id(affected_ver):

                G.add_edge(affected_req, affected_ver)

            if valid_id(affected_ver) and valid_id(affected_test):

                G.add_edge(affected_ver, affected_test)

        print("Nodes =", G.number_of_nodes())
        print("Edges =", G.number_of_edges())
        
        print("=== BUILD END ===")
        ##################################################
        # Remove Invalid Nodes
        ##################################################
        
        invalid_nodes = [
            n for n in G.nodes
            if not isinstance(n, (str, int))
        ]
        
        if invalid_nodes:
            print("REMOVE INVALID NODES:", invalid_nodes)
            G.remove_nodes_from(invalid_nodes)

        ##################################################
        # Remove Invalid Edges
        ##################################################
        
        for u, v in list(G.edges()):
        
            if (
                not isinstance(u, (str, int))
                or
                not isinstance(v, (str, int))
            ):
        
                G.remove_edge(u, v)

        bad_nodes = [
        n for n in G.nodes
        if not isinstance(n, (str, int))
            
        ]
        
        if bad_nodes:
            print("REMOVE:", bad_nodes)
            G.remove_nodes_from(bad_nodes)
            
        return G, rkg_df.head()
