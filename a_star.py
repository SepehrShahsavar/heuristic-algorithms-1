from xmlrpc.client import MAXINT
from plot_G import plot_G


# TODO: Reading from file: reading edges alongside heuristic values and costs of each edge

def get_edges():
    n = int(input("Enter the number of edges : "))
    edges = []
    edge_costs = {}
    for i in range(n):
        line = input(
            "Enter an edge ({}) with its cost : ".format(i + 1)).split()
        start, end, cost = line[0], line[2], int(line[3])
        edge = (start, end)
        edges.append(edge)
        edge_costs[edge] = cost
    return edges, edge_costs


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


edges, edge_costs = get_edges()
nodes = find_nodes(edges)
heu_distances = get_heu_distances(nodes)
start, goal = find_start(edges, nodes), find_goal(edges, nodes)

current = start

status = {}
for node in nodes:
    status[node] = "not visited"

status[current] = "current"

shortest_distance_from_start = {}
shortest_distance_from_start[current] = 0

total_distances = {}
total_distances[current] = shortest_distance_from_start[current] + \
    heu_distances[current]

previous_node = {}

possible_next_nodes = []


while current != goal:
    childs = get_childs(current)

    for child in childs:
        if child not in possible_next_nodes:
            possible_next_nodes.append(child)
            status[child] = "possible"
            previous_node[child] = current
            shortest_distance_from_start[child] = shortest_distance_from_start[current] + \
                edge_costs[(current, child)]
            total_distances[child] = shortest_distance_from_start[child] + \
                heu_distances[child]
        else:
            temp = shortest_distance_from_start[current] + \
                edge_costs[(current, child)] + heu_distances[child]
            if total_distances[child] > temp:
                shortest_distance_from_start[child] = shortest_distance_from_start[current] + \
                    edge_costs[(current, child)]
                total_distances[child] = temp
                previous_node[child] = current

    min_node = None
    min_distance = MAXINT
    for node in possible_next_nodes:
        if total_distances[node] < min_distance:
            min_distance = total_distances[node]
            min_node = node

    show_graph()
    possible_next_nodes.remove(min_node)
    status[current] = "visited"
    current = min_node
    status[current] = "current"

show_graph()
