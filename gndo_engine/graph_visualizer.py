from pyvis.network import Network
import tempfile


class GraphVisualizer:

    @staticmethod
    def build_network(
        G,
        height="800px",
        width="100%"
    ):

        net = Network(
            height=height,
            width=width,
            bgcolor="#ffffff",
            font_color="black",
            directed=True
        )

        net.from_nx(G)

        ##################################################
        # Node Color
        ##################################################

        color_map = {
            "CHANGE": "#ff0000",
            "REQ": "#00cc66",
            "VER": "#0099ff",
            "TEST": "#ffaa00",
            "FAIL": "#9900cc"
        }

        for node in net.nodes:

            node_type = node.get("type")

            if node_type in color_map:
                node["color"] = color_map[node_type]

            node["shape"] = "dot"
            node["size"] = 18

        ##################################################
        # Edge Style
        ##################################################

        for edge in net.edges:

            edge["width"] = 3

            edge["arrows"] = "to"

            edge["smooth"] = {
                "type": "dynamic"
            }

            edge["font"] = {
                "size": 14,
                "align": "middle"
            }

        return net

    ##################################################

    @staticmethod
    def save_html(net):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".html"
        ) as tmp:

            net.save_graph(tmp.name)

            with open(
                tmp.name,
                encoding="utf-8"
            ) as f:

                html = f.read()

        return html
