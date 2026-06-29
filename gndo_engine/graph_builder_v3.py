import networkx as nx
import pandas as pd


class GraphBuilderV3:

    @staticmethod
    def build(rkg_df):

        print("======================================")
        print("GNDO GraphBuilder V3")
        print("======================================")

        G = nx.DiGraph()

        node_types = {
            "requirement_id": "REQ",
            "verification_id": "VER",
            "test_id": "TEST",
            "failure_id": "FAIL",
            "change_id": "CHANGE"
        }
        ##################################################
        # Build Nodes
        ##################################################

        for _, row in rkg_df.iterrows():

            chapter = row.get("chapter")

            for column, node_type in node_types.items():

                node_id = row.get(column)

                if pd.notna(node_id):

                    G.add_node(
                        str(node_id),
                        type=node_type,
                        label=str(node_id),
                        chapter=chapter
                    )
        ##################################################
        # Requirement → Verification
        ##################################################
        
            if (
                pd.notna(row.get("requirement_id"))
                and
                pd.notna(row.get("verification_id"))
            ):

                G.add_edge(
                    str(row["requirement_id"]),
                    str(row["verification_id"]),
                    relation="verified_by"
                )

        ##################################################
        # Verification → Test
        ##################################################
        
            if (
                pd.notna(row.get("verification_id"))
                and
                pd.notna(row.get("test_id"))
            ):

                G.add_edge(
                    str(row["verification_id"]),
                    str(row["test_id"]),
                    relation="tested_by"
                )

        ##################################################
        # Test → Failure
        ##################################################
        
            if (
                pd.notna(row.get("test_id"))
                and
                pd.notna(row.get("failure_id"))
            ):

                G.add_edge(
                    str(row["test_id"]),
                    str(row["failure_id"]),
                    relation="failure_mode"
                )

        ##################################################
        # Requirement → Failure
        ##################################################
        
            if (
                pd.notna(row.get("requirement_id"))
                and
                pd.notna(row.get("failure_id"))
            ):

                G.add_edge(
                    str(row["requirement_id"]),
                    str(row["failure_id"]),
                    relation="causes"
                )

        ##################################################
        # Change → Requirement
        ##################################################
        
            if (
                pd.notna(row.get("change_id"))
                and
                pd.notna(row.get("affected_requirement"))
            ):

                G.add_edge(
                    str(row["change_id"]),
                    str(row["affected_requirement"]),
                    relation="changes"
                )

        ##################################################
        # Requirement → Verification (Impact)
        ##################################################
        
            if (
                pd.notna(row.get("affected_requirement"))
                and
                pd.notna(row.get("affected_verification"))
            ):

                G.add_edge(
                    str(row["affected_requirement"]),
                    str(row["affected_verification"]),
                    relation="reverify"
                )

        ##################################################
        # Verification → Test (Impact)
        ##################################################
        
            if (
                pd.notna(row.get("affected_verification"))
                and
                pd.notna(row.get("affected_test"))
            ):

                G.add_edge(
                    str(row["affected_verification"]),
                    str(row["affected_test"]),
                    relation="retest"
                )

        ##################################################
        # Summary
        ##################################################

        print()

        print("======================================")
        print("Graph Summary")
        print("======================================")

        counts = {}

        for _, attr in G.nodes(data=True):

            node_type = attr.get("type")

            counts[node_type] = counts.get(node_type, 0) + 1

        for t in ["REQ", "VER", "TEST", "FAIL", "CHANGE"]:

            print(f"{t:7}: {counts.get(t,0)}")

        print("--------------------------------------")
        print("Total Nodes :", G.number_of_nodes())
        print("Total Edges :", G.number_of_edges())
        print("======================================")

        return G

    @staticmethod
    def build_impact_graph(row):

        G = nx.DiGraph()

        change = row.get("change_id")
        req = row.get("affected_requirement")
        ver = row.get("affected_verification")
        test = row.get("affected_test")
        fail = row.get("failure_id")

        if pd.notna(change):
            G.add_node(str(change), type="CHANGE")

        if pd.notna(req):
            G.add_node(str(req), type="REQ")

        if pd.notna(ver):
            G.add_node(str(ver), type="VER")

        if pd.notna(test):
            G.add_node(str(test), type="TEST")

        if pd.notna(fail):
            G.add_node(str(fail), type="FAIL")

        if pd.notna(change) and pd.notna(req):
            G.add_edge(str(change), str(req))

        if pd.notna(req) and pd.notna(ver):
            G.add_edge(str(req), str(ver))

        if pd.notna(ver) and pd.notna(test):
            G.add_edge(str(ver), str(test))

        if pd.notna(test) and pd.notna(fail):
            G.add_edge(str(test), str(fail))

        return G
