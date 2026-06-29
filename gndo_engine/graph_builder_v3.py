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

            for column, node_type in node_types.items():

                node_id = row.get(column)

                if pd.notna(node_id):

                    G.add_node(
                        str(node_id),
                        type=node_type,
                        label=str(node_id),
                        chapter=row.get("chapter")
                    )
