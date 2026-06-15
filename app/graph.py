import json
import networkx as nx

def build_graph():

    with open(
        "storage/metadata/crosswalk_data.json",
        "r",
        encoding="utf-8"
    ) as f:

        links = json.load(f)

    G = nx.Graph()

    for item in links:

        srp = item["srp"]
        ap1000 = item["ap1000"]
        apr1400 = item["apr1400"]

        G.add_node(
            srp,
            group="SRP"
        )

        G.add_node(
            ap1000,
            group="AP1000"
        )

        G.add_node(
            apr1400,
            group="APR1400"
        )

        G.add_edge(
            srp,
            ap1000
        )

        G.add_edge(
            ap1000,
            apr1400
        )

    return G
