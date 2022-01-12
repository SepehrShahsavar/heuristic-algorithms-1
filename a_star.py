from plot_G import plot_G


def get_input():
    n = int(input("Enter the number of edges : "))
    edges = []
    for i in range(n):
        line = input("Enter an edge ({}): ".format(i + 1)).split()
        start, end = line[0], line[2]
        edges.append((start, end))
    return edges


def find_nodes(edges):
    nodes = {}
    for edge in edges:
        nodes[edge[0]] = "purple"
        nodes[edge[1]] = "purple"
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


edges = get_input()
nodes = find_nodes(edges)
start, goal = find_start(edges, nodes), find_goal(edges, nodes)
