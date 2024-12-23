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
