
def parse_rules(rule_list):
  rules = [(int(r.split('|')[0]), int(r.split('|')[1])) for r in rule_list]

  # sorted rules
  s = {}

  for r in rules:
    if r[0] in s:
      s[r[0]]['after'].append(r[1])
    else:
      s[r[0]] = {'after':[r[1]], 'before':[]}
    if r[1] in s:
      s[r[1]]['before'].append(r[0])
    else:
      s[r[1]] = {'before':[r[0]], 'after':[]}

  return s

def check_update_order(update, rules):

  for i, n in enumerate(update):
    b = update[:i]
    a = update[i+1:]
    if any(i in rules[n]['before'] for i in a): return False
    if any(i in rules[n]['after'] for i in b): return False

  return True

def bubble(update, rules):

  swapped_flag = True
  sorted = update.copy()
  while swapped_flag:
    swapped_flag = False
    for i in range(len(sorted)-1):
      x = sorted[i]
      y = sorted[i+1]
      if x in rules[y]['after'] or y in rules[x]['before']:
        # swap
        sorted[i] = y
        sorted[i+1] = x
        swapped_flag = True

  return sorted

def main():

  fname = 'input.txt'

  rules = []
  updates = []
  with open(fname, 'r') as file:
    line = file.readline()
    while line and line != '\n':
      rules.append(line.strip())
      line = file.readline()
    for line in file:
      updates.append([int(i) for i in line.strip().split(',')])

  rule_lu  = parse_rules(rules)

  total = 0
  to_sort = []
  for i, u in enumerate(updates):
    middle_ind = len(u)//2

    if check_update_order(u, rule_lu):
      total += u[middle_ind]
    else:
      to_sort.append(i)

  print("Part 1: ", total)

  # Part 2

  total = 0
  for i in to_sort:
    sorted = bubble(updates[i], rule_lu)

    total += sorted[len(sorted)//2]
  print("Part 2: ", total)

if __name__ == '__main__':
  main()
