import networkx as nx
import pandas as pd


class GraphBuilderV3:

    @staticmethod
    def build(rkg_df):

        print("======================================")
        print("GNDO GraphBuilder V3")
        print("======================================")

        G = nx.DiGraph()

        ##################################################
        # Build Nodes
        ##################################################

        for _, row in rkg_df.iterrows():

            req = row.get("requirement_id")
            ver = row.get("verification_id")
            test = row.get("test_id")
            fail = row.get("failure_id")
            change = row.get("change_id")

            chapter = row.get("chapter")

            ##################################################
            # Requirement
            ##################################################

            if pd.notna(req):

                G.add_node(
                    str(req),
                    type="REQ",
                    label=str(req),
                    chapter=chapter
                )

            ##################################################
            # Verification
            ##################################################

            if pd.notna(ver):

                G.add_node(
                    str(ver),
                    type="VER",
                    label=str(ver),
                    chapter=chapter
                )

            ##################################################
            # Test
            ##################################################

            if pd.notna(test):

                G.add_node(
                    str(test),
                    type="TEST",
                    label=str(test),
                    chapter=chapter
                )

            ##################################################
            # Failure
            ##################################################

            if pd.notna(fail):

                G.add_node(
                    str(fail),
                    type="FAIL",
                    label=str(fail),
                    chapter=chapter
                )

            ##################################################
            # Change
            ##################################################

            if pd.notna(change):

                G.add_node(
                    str(change),
                    type="CHANGE",
                    label=str(change),
                    chapter=chapter
                )
