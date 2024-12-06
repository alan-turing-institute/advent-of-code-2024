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


def calculate_sum_of_middle_pages(rules, updates):
    correctly_ordered_updates = []
    for update in updates:
        if is_update_ordered(update, rules):
            correctly_ordered_updates.append(update)

    middle_pages_sum = sum(
        find_middle_page(update) for update in correctly_ordered_updates
    )
    return middle_pages_sum


def main():
    # Read and parse input
    rules, updates = parse_input("input.txt")

    # Calculate the sum of middle pages
    result = calculate_sum_of_middle_pages(rules, updates)

    print(f"Sum of middle pages of correctly ordered updates: {result}")


if __name__ == "__main__":
    main()
