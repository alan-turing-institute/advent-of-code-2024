import networkx as nx


def parse_input(input_file):
    with open(input_file, "r") as f:
        lines = f.read().splitlines()
    return lines


def parse_data(data):
    G = nx.Graph()
    for line in data:
        line = line.strip()
        line = line.split("-")
        G.add_edge(line[0], line[1])

    return G

def nodes_connected(G, u, v):
    return u in G.neighbors(v)

if __name__ == "__main__":

    data = parse_input("input.txt")
    #data = parse_input("test.txt")

    G = parse_data(data)

    interconected = set()
    for node1 in G.nodes():
        for node2 in G.nodes():
            if node1 != node2:
                if nodes_connected(G,node1,node2):
                    common_neighbors = list(nx.common_neighbors(G, node1, node2))
                    for common_neighbor in common_neighbors:
                        if common_neighbor.startswith("t") or node1.startswith("t") or node2.startswith("t"):
                            interconected.add(tuple(sorted([node1, node2, common_neighbor])))


    cliques = list(nx.enumerate_all_cliques(G))


    max = 0
    for i in range(len(cliques)):
        if len(cliques[i]) > max:
            max = len(cliques[i])
            index_max = i


    print(','.join(sorted(cliques[index_max])))




