import networkx as nx
import matplotlib.pyplot as plt


def plot_G(edges, node_color_map):
    G = nx.DiGraph()
    G.add_edges_from(edges)
    node_colors = [node_color_map.get(node) for node in G.nodes()]
    pos = nx.spring_layout(G)

    nx.draw_networkx_nodes(G, pos,
                           node_color=node_colors, node_size=500)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color="black")
    nx.draw_networkx_labels(G, pos)

    plt.show()
