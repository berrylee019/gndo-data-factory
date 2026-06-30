import pandas as pd

from gndo_engine.graph_builder_v3 import GraphBuilderV3


class TraceabilityEngine:

    def __init__(self, rkg_df):

        self.rkg_df = rkg_df
      

    def find_change(self, change_id):

    rows = self.rkg_df[
        self.rkg_df["change_id"] == change_id
    ]

    if rows.empty:

        return None

    return rows.iloc[0]
  

    def build_change_graph(self, change_id):

        row = self.find_change(change_id)

        if row is None:

            return None

        return GraphBuilderV3.build_impact_graph(row)
