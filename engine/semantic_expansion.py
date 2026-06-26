import pandas as pd


class SemanticExpansion:

    @staticmethod
    def same_system(req_id, rkg_df):

        semantic_nodes = set()

        rows = rkg_df[
            rkg_df["requirement_id"] == req_id
        ]

        if rows.empty:
            return semantic_nodes

        system = rows.iloc[0].get("system_id")

        if pd.isna(system):
            return semantic_nodes

        same = rkg_df[
            rkg_df["system_id"] == system
        ]

        semantic_nodes.update(
            same["requirement_id"]
            .dropna()
            .tolist()
        )

        return semantic_nodes
