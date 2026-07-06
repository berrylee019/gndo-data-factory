from pyvis.network import Network
import tempfile

NODE_STYLE = {

    "CHANGE": {
        "color": "#ff3b30",
        "size": 36,
        "shape": "dot"
    },

    "REQ": {
        "color": "#34c759",
        "size": 32,
        "shape": "dot"
    },

    "VER": {
        "color": "#ffcc00",
        "size": 30,
        "shape": "dot"
    },

    "TEST": {
        "color": "#007aff",
        "size": 30,
        "shape": "dot"
    },

    "FAIL": {
        "color": "#8e24aa",
        "size": 32,
        "shape": "dot"
    },

    "SYSTEM": {
        "color": "#26c6da",
        "size": 26,
        "shape": "box"
    },

    "ARTIFACT": {
        "color": "#9e9e9e",
        "size": 24,
        "shape": "box"
    }

}


class GraphVisualizer:

    @staticmethod
    def build_network(G):

        net = Network(
            height="650px",
            width="100%",
            directed=True,
            bgcolor="#ffffff",
            font_color="#222222"
        )

        for node, attr in G.nodes(data=True):

            style = NODE_STYLE.get(
                attr.get("type"),
                {
                    "color":"#cccccc",
                    "size":25,
                    "shape":"dot"
                }
            )

            net.add_node(
                node,
                label=node,
                color=style["color"],
                size=style["size"],
                shape=style["shape"]
            )

        for u, v, attr in G.edges(data=True):

            net.add_edge(
                u,
                v,
                arrows="to",
                color="#666666",
                width=2
            )

        net.toggle_physics(True)

        return net


    @staticmethod
    def save_html(net):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".html"
        ) as tmp:

            net.save_graph(tmp.name)

            return open(
                tmp.name,
                encoding="utf-8"
            ).read()
