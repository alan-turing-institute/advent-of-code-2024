import sys


def concatenate(num1, num2):
    return int(f'{num1}{num2}')


def aggregate(numbers, allow_concatenation=False):
    def _aggregate(numbers, result):
        if len(numbers) == 2:
            result.append(numbers[0] * numbers[1])
            result.append(numbers[0] + numbers[1])

            if allow_concatenation:
                result.append(concatenate(numbers[0], numbers[1]))

            return

        _aggregate([numbers[0] + numbers[1], *numbers[2:]], result)
        _aggregate([numbers[0] * numbers[1], *numbers[2:]], result)

        if allow_concatenation:
            _aggregate([concatenate(numbers[0], numbers[1]), *numbers[2:]], result)

    result = []
    _aggregate(numbers, result)

    return result


def part1(contents):
    operations = [(int(line.split(':')[0]), [int(val) for val in line.split(':')[1].split()])
                  for line in contents.split('\n') if line]

    calibrations = 0
    for test_val, numbers in operations:
        for agg in aggregate(numbers):
            if agg == test_val:
                calibrations += test_val
                break

    return calibrations


def part2(contents):
    operations = [(int(line.split(':')[0]), [int(val) for val in line.split(':')[1].split()])
                  for line in contents.split('\n') if line]

    calibrations = 0
    for test_val, numbers in operations:
        for agg in aggregate(numbers, allow_concatenation=True):
            if agg == test_val:
                calibrations += test_val
                break

    return calibrations


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as fh:
        contents = fh.read()

    print('Solution to part 1:', part1(contents))
    print('Solution to part 2:', part2(contents))
