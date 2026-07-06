import networkx as nx
import pandas as pd

print("GraphBuilderV3 VERSION = 2026-06-29 V3")

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
    
        # -------------------------
        # Nodes
        # -------------------------
    
        nodes = {
            "cfr": row.get("cfr"),
            "rg": row.get("rg"),
            "nureg": row.get("nureg"),
            "srp": row.get("srp"),
    
            "requirement": row.get("requirement_id"),
            "verification": row.get("verification_id"),
            "test": row.get("test_id"),
            "failure": row.get("failure_id"),
    
            "artifact": row.get("artifact_id"),
            "system": row.get("system_id"),
            "component": row.get("component_id"),
    
            "ap1000": row.get("ap1000"),
            "apr1400": row.get("apr1400"),
    
            "change": row.get("change_id")
        }
    
        for node_type, node_id in nodes.items():
    
            if pd.notna(node_id):
    
                G.add_node(
                    str(node_id),
                    type=node_type.upper(),
                    label=str(node_id)
                )
    
        # -------------------------
        # Regulatory Chain
        # -------------------------
    
        def edge(a, b, relation):
    
            if pd.notna(a) and pd.notna(b):
    
                G.add_edge(
                    str(a),
                    str(b),
                    relation=relation
                )
    
        edge(nodes["cfr"], nodes["rg"], "IMPLEMENTED_BY")
        edge(nodes["rg"], nodes["nureg"], "GUIDES")
        edge(nodes["nureg"], nodes["srp"], "REVIEWED_BY")
    
        edge(nodes["srp"], nodes["requirement"], "GENERATES")
    
        edge(nodes["requirement"], nodes["verification"], "VERIFIED_BY")
    
        edge(nodes["verification"], nodes["test"], "TESTED_BY")
    
        edge(nodes["test"], nodes["artifact"], "DOCUMENTED_BY")
    
        edge(nodes["test"], nodes["system"], "VALIDATES")
    
        edge(nodes["system"], nodes["component"], "CONTAINS")
    
        edge(nodes["artifact"], nodes["system"], "IMPLEMENTS")
    
        edge(nodes["requirement"], nodes["failure"], "CAUSES")
    
        edge(nodes["change"], row.get("affected_requirement"), "CHANGES")
    
        edge(
            row.get("affected_requirement"),
            row.get("affected_verification"),
            "REVERIFY"
        )
    
        edge(
            row.get("affected_verification"),
            row.get("affected_test"),
            "RETEST"
        )
    
        edge(nodes["srp"], nodes["ap1000"], "APPLIED_TO")
    
        edge(nodes["ap1000"], nodes["apr1400"], "EQUIVALENT_TO")
    
        return G
