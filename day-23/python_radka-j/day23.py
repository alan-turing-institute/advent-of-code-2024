from collections import defaultdict

with open("input.txt") as f:
    lines = f.read().splitlines()

graph = defaultdict(list)
for line in lines:
    node1, node2 = line.split("-")
    graph[node1].append(node2)
    graph[node2].append(node1)


# PART 1 - very lazy

connections = []
for node in graph:
    if node[0] == "t":
        neighbours = graph[node]
        for node2 in neighbours:
            neighbours2 = graph[node2]
            for node3 in neighbours2:
                if node3 in neighbours:
                    connections.append(tuple(sorted((node, node2, node3))))

print(len(set(connections)))

# PART 2: https://en.wikipedia.org/wiki/Bron–Kerbosch_algorithm
#
# To start, set R and X to be the empty set and P to be the set of all nodes in the graph
# then consider each node in P one at a time (N[v] are the neighbours of node v)
#
# algorithm BronKerbosch(R, P, X) is
#     if P and X are both empty then
#         report R as a maximal clique
#     for each vertex v in P do
#         BronKerbosch1(R ⋃ {v}, P ⋂ N(v), X ⋂ N(v))
#         P := P \ {v}
#         X := X ⋃ {v}


def bronkerbosch(R, P, X):
    if len(P) == 0 and len(X) == 0:
        return [R]
    cliques = []
    for node in list(P):
        neighbours = set(graph[node])
        cliques += bronkerbosch(
            set(R).union({node}),
            set(P).intersection(neighbours),
            set(X).intersection(neighbours),
        )
        X.add(node)
        P.remove(node)
    return cliques


all_cliques = bronkerbosch(set(), set(graph.keys()), set())
for clique in all_cliques:
    # from looking at the output, know that the biggest clique has length 13
    if len(clique) > 12:
        print(sorted(clique))
