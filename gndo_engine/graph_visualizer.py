from pyvis.network import Network
import tempfile

NODE_STYLE = {
    "CHANGE": {"color": "#ff3b30", "size": 36, "shape": "dot"},
    "REQ": {"color": "#34c759", "size": 32, "shape": "dot"},
    "VER": {"color": "#ffcc00", "size": 30, "shape": "dot"},
    "TEST": {"color": "#007aff", "size": 30, "shape": "dot"},
    "FAIL": {"color": "#8e24aa", "size": 32, "shape": "dot"},
    "SYSTEM": {"color": "#26c6da", "size": 26, "shape": "box"},
    "ARTIFACT": {"color": "#9e9e9e", "size": 24, "shape": "box"},
}

EDGE_STYLE = {
    "changes": {"color": "#ff3b30", "width": 5},
    "verified_by": {"color": "#34c759", "width": 4},
    "tested_by": {"color": "#007aff", "width": 4},
    "failure_mode": {"color": "#8e24aa", "width": 4},
    "causes": {"color": "#ff9500", "width": 3},
    "reverify": {"color": "#00c853", "width": 3, "dashes": True},
    "retest": {"color": "#2962ff", "width": 3, "dashes": True},
}


class GraphVisualizer:

    @staticmethod
    def build_network(G, highlight_nodes=None):

        if highlight_nodes is None:
            highlight_nodes = set()

        net = Network(
            height="650px",
            width="100%",
            directed=True,
            bgcolor="#ffffff",
            font_color="#222222",
        )

        # ---------- Nodes ----------
        for node, attr in G.nodes(data=True):

            style = NODE_STYLE.get(
                attr.get("type"),
                {
                    "color": "#cccccc",
                    "size": 25,
                    "shape": "dot",
                },
            )

            node_color = style["color"]

            if highlight_nodes and node not in highlight_nodes:
                node_color = "#d9d9d9"

            tooltip = f"<b>{node}</b><br><hr>"
            
            fields = [
                "chapter",
                "topic",
                "system",
                "component",
                "requirement",
                "verification",
                "verification_method",
                "acceptance",
                "test",
                "artifact",
                "failure",
                "severity",
                "consequence",
                "mitigation",
            ]
            
            for field in fields:
            
                value = attr.get(field)
            
                if value not in [None, "", "nan"]:
            
                    tooltip += f"<b>{field}</b> : {value}<br>"
            
            net.add_node(
                str(node),
                label=str(attr.get("label", node)),
                color=style["color"],
                size=style["size"],
                shape=style["shape"],
                title=tooltip
            )

        # ---------- Edges ----------
        for u, v, attr in G.edges(data=True):

            relation = attr.get("relation", "")

            style = EDGE_STYLE.get(
                relation,
                {
                    "color": "#888888",
                    "width": 2,
                },
            )

            edge_color = style["color"]

            if highlight_nodes:
                if u not in highlight_nodes or v not in highlight_nodes:
                    edge_color = "#d9d9d9"

            net.add_edge(
                str(u),
                str(v),
                arrows="to",
                color=edge_color,
                width=style["width"],
                dashes=style.get("dashes", False),
                title=relation,
                smooth={"type": "dynamic"},
            )

        net.toggle_physics(True)

        return net

    @staticmethod
    def save_html(net):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".html",
        ) as tmp:

            net.save_graph(tmp.name)

            with open(tmp.name, encoding="utf-8") as f:
                return f.read()
