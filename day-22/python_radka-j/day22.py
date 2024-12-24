from collections import defaultdict

with open("input.txt") as f:
    lines = f.read().splitlines()

init_numbers = [int(n) for n in lines]

# PART 1

tot = 0
for num in init_numbers:
    for i in range(2000):
        num = ((num * 64) ^ num) % 16777216
        num = ((num // 32) ^ num) % 16777216
        num = ((num * 2048) ^ num) % 16777216
    tot += num

print("part 1: ", tot)


# PART 2
# find the sequence of 4 number changes that maximizes the bananas sold across all buyers

secret_nums = []
for num in init_numbers:
    vals = [num]
    for i in range(2000):
        num = ((num * 64) ^ num) % 16777216
        num = ((num // 32) ^ num) % 16777216
        num = ((num * 2048) ^ num) % 16777216

        # get the last digit of the number
        val = int(str(num)[-1])
        vals.append(val)
    secret_nums.append(vals)


sequence_price = defaultdict(list)
for nums in secret_nums:
    # want to get the price the first time that see a sequence for each buyer
    # this is equivalent to a list of visited
    sequences = []

    differences = [nums[i + 1] - nums[i] for i in range(len(nums) - 1)]
    # sliding window with size 4
    for i in range(len(differences) - 4 + 1):
        sequence = differences[i : i + 4]
        if sequence not in sequences:
            sequence_price[tuple(sequence)].append(nums[i + 4])
            sequences.append(sequence)


max_val = 0
for seq, prices in sequence_price.items():
    if sum(prices) > max_val:
        max_val = sum(prices)

print(max_val)
