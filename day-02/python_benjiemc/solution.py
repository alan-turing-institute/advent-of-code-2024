import sys


def part1(contents):
    reports = [[int(level) for level in report.split()] for report in contents.split('\n') if report]

    safe_count = 0

    for report in reports:

        sign = None
        for level1, level2 in zip(report[:-1], report[1:]):
            delta = level2 - level1

            if sign is None:
                sign = 'positive' if delta > 0 else 'negative'

            elif sign == 'positive' and delta < 0:
                break

            elif sign == 'negative' and delta > 0:
                break

            if abs(delta) == 0 or abs(delta) > 3:
                break

        else:
            safe_count += 1

    return safe_count


def check_report(report, rescue=True):
    sign = None
    for level1, level2 in zip(report[:-1], report[1:]):
        delta = level2 - level1

        if sign is None:
            sign = 'positive' if delta > 0 else 'negative'

        elif sign == 'positive' and delta < 0:
            break

        elif sign == 'negative' and delta > 0:
            break

        if abs(delta) == 0 or abs(delta) > 3:
            break

    else:
        return True

    if rescue:
        for i in range(len(report)):
            new_report = report[:i] + report[i + 1:]

            if check_report(new_report, rescue=False):
                return True

    return False


def part2(contents):
    reports = [[int(level) for level in report.split()] for report in contents.split('\n') if report]

    safe_count = 0

    for report in reports:
        if check_report(report):
            safe_count += 1

    return safe_count


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as fh:
        contents = fh.read()

    print('Part one solution:', part1(contents))
    print('Part two solution:', part2(contents))
