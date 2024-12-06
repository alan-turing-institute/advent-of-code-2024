from collections import defaultdict, deque


def parse_input(filename):
    with open(filename, "r") as file:
        lines = file.read().strip().split("\n")

    # Split rules and updates
    rules = []
    updates = []
    parsing_rules = True
    for line in lines:
        if line == "":
            parsing_rules = False
            continue
        if parsing_rules:
            rules.append(tuple(map(int, line.split("|"))))
        else:
            updates.append(list(map(int, line.split(","))))

    return rules, updates


def is_update_ordered(update, rules):
    # Create a mapping of page indices
    page_index = {page: idx for idx, page in enumerate(update)}

    for x, y in rules:
        if x in page_index and y in page_index:
            if page_index[x] > page_index[y]:
                return False
    return True


def find_middle_page(update):
    mid_idx = len(update) // 2
    return update[mid_idx]


def fix_update_order(update, rules):
    # Build a graph based on rules
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    update_set = set(update)

    # Add edges only for pages in this update
    for x, y in rules:
        if x in update_set and y in update_set:
            graph[x].append(y)
            in_degree[y] += 1
            if x not in in_degree:
                in_degree[x] = 0

    # Perform topological sort (Kahn's Algorithm)
    queue = deque([node for node in update if in_degree[node] == 0])
    sorted_update = []

    while queue:
        node = queue.popleft()
        sorted_update.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_update


def calculate_sum_of_middle_pages_part2(rules, updates):
    incorrectly_ordered_updates = []
    for update in updates:
        if not is_update_ordered(update, rules):
            incorrectly_ordered_updates.append(update)

    fixed_updates = [
        fix_update_order(update, rules) for update in incorrectly_ordered_updates
    ]
    middle_pages_sum = sum(find_middle_page(update) for update in fixed_updates)

    return middle_pages_sum


def main():
    # Read and parse input
    rules, updates = parse_input("input.txt")

    # Calculate the sum of middle pages for incorrectly ordered updates after fixing them
    result = calculate_sum_of_middle_pages_part2(rules, updates)

    print(f"Sum of middle pages of fixed updates: {result}")


if __name__ == "__main__":
    main()
