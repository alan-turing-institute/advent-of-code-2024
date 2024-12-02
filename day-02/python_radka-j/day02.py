with open("input.txt") as f:
    lines = f.read().splitlines()

reports = [[int(char) for char in l.split(" ")] for l in lines]


def safe(report):
    increase = [l1 < l2 for l1, l2 in zip(report[:-1], report[1:])]
    decrease = [l1 > l2 for l1, l2 in zip(report[:-1], report[1:])]
    unsafe_diff = [abs(l1 - l2) > 3 for l1, l2 in zip(report[:-1], report[1:])]

    if (all(increase) or all(decrease)) and not any(unsafe_diff):
        return True
    return False


safe_count_part1 = 0
safe_count_part2 = 0

for report in reports:
    if safe(report):
        safe_count_part1 += 1
        safe_count_part2 += 1
    else:
        # investigate whether dropping any level can make the report safe
        for i in range(len(report)):
            drop_level = report[:i] + report[i + 1 :]
            if safe(drop_level):
                safe_count_part2 += 1
                break


print("part 1: ", safe_count_part1)
print("part 2: ", safe_count_part2)
