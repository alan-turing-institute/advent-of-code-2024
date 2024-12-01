import pandas as pd
df = pd.read_csv('advent_of_code.csv',header=None, names=['list1', 'list2'])

list1 = df['list1'].to_list()
total_list = [df[df['list2'] == val].shape[0] * val for val in list1]

print(sum(total_list))

