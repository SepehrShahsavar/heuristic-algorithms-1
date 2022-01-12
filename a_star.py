from plot_G import plot_G


# TODO: Reading from file: reading edges alongside heuristic values and costs of each edge

def get_input():
    n = int(input("Enter the number of edges : "))
    edges = []
    for i in range(n):
        line = input("Enter an edge ({}) with its cost : ".format(i + 1)).split()
        start, end, cost = line[0], line[2], int(line[3])
        edges.append(((start, end), cost))
    nodes = find_nodes(edges)
    new_nodes = {}
    for node in nodes:
        heu_cost = int(input("Enter the heuristic value of node {} : ".format(node)))
        new_nodes[(node, heu_cost)] = nodes[node]
    return edges, new_nodes


def find_nodes(edges):
    nodes = {}
    for edge in edges:
        nodes[edge[0][0]] = "purple"
        nodes[edge[0][1]] = "purple"
    return nodes


def find_start(edges, nodes):
    for node in nodes:
        is_end = False
        for edge in edges:
            if node[0] == edge[0][1]:
                is_end = True
                break
        if is_end == False:
            return node


def find_goal(edges, nodes):
    for node in nodes:
        is_start = False
        for edge in edges:
            if node[0] == edge[0][0]:
                is_start = True
                break
        if is_start == False:
            return node





edges, nodes = get_input()
start, goal = find_start(edges, nodes), find_goal(edges, nodes)
print(edges)
print(nodes)
print(start, goal)
