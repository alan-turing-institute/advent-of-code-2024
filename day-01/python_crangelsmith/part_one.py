import pandas as pd
df = pd.read_csv('advent_of_code.csv',header=None, names=['list1', 'list2'])

sorted_list1 = sorted(df['list1'].to_list())
sorted_list2 = sorted(df['list2'].to_list())

difference = [abs(l1_i - l2_i) for l1_i, l2_i in zip(sorted_list1, sorted_list2)]

print(sum(difference))
