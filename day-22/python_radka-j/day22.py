with open("input.txt") as f:
    lines = f.read().splitlines()

init_numbers = [int(n) for n in lines]

tot = 0
for num in init_numbers:
    for i in range(2000):
        num = ((num * 64) ^ num) % 16777216
        num = ((num // 32) ^ num) % 16777216
        num = ((num * 2048) ^ num) % 16777216
    tot += num
print(tot)
