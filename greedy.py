from xmlrpc.client import MAXINT
from plot_G import plot_G


def get_edges():
    n = int(input("Enter the number of edges : "))
    edges = []
    for i in range(n):
        line = input(
            "Enter an edge ({}) : ".format(i + 1)).split()
        start, end = line[0], line[2]
        edge = (start, end)
        edges.append(edge)
    return edges


def get_heu_distances(nodes):
    heu_distances = {}
    for node in nodes:
        heu_distance = int(
            input("Enter the heuristic distance of node {} : ".format(node)))
        heu_distances[node] = heu_distance
    return heu_distances


def find_nodes(edges):
    nodes = []
    for edge in edges:
        if edge[0] not in nodes:
            nodes.append(edge[0])
        if edge[1] not in nodes:
            nodes.append(edge[1])
    return nodes


def find_start(edges, nodes):
    for node in nodes:
        is_end = False
        for edge in edges:
            if node == edge[1]:
                is_end = True
                break
        if is_end == False:
            return node


def find_goal(edges, nodes):
    for node in nodes:
        is_start = False
        for edge in edges:
            if node == edge[0]:
                is_start = True
                break
        if is_start == False:
            return node


def get_childs(node):
    childs = []
    for edge in edges:
        if node == edge[0]:
            childs.append(edge[1])
    return childs


def show_graph():
    node_color_map = {}
    for node in status.keys():
        if status[node] == "not visited":
            node_color_map[node] = "purple"
        elif status[node] == "current":
            node_color_map[node] = "green"
        elif status[node] == "possible":
            node_color_map[node] = "cyan"
        elif status[node] == "visited":
            node_color_map[node] = "grey"
    plot_G(edges, node_color_map)


edges = get_edges()
nodes = find_nodes(edges)
heu_distances = get_heu_distances(nodes)
start, goal = find_start(edges, nodes), find_goal(edges, nodes)

current = start

status = {}
for node in nodes:
    status[node] = "not visited"

status[current] = "current"

previous_node = {}

while current != goal:
    childs = get_childs(current)

    min_node = None
    min_distance = MAXINT
    for child in childs:
        status[child] = "possible"
        previous_node[child] = current
        if heu_distances[child] < min_distance:
            min_distance = heu_distances[child]
            min_node = child

    show_graph()

    for child in childs:
        if child != min_node:
            status[child] = "not visited"

    status[current] = "visited"
    current = min_node
    status[current] = "current"

show_graph()
