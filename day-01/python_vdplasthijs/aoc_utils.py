import numpy as np

def read_txt_file_lines(filename='input.txt', read_arg='r'):
    with open(filename, read_arg) as f:
        return [line.strip() for line in f.readlines()]

def read_txt_file_lines_ints(filename='input.txt', read_arg='r'):
    with open(filename, read_arg) as f:
        return [[int(x) for x in line.split()] for line in f.readlines()]
    
def read_txt_file_without_escape(filename='input.txt', read_arg='r'):
    with open(filename, read_arg) as f:
        return f.read().strip()
    
def gcd(a, b):
    """find common divisor of all diffs"""   
    while b:
        a, b = b, a % b
    return a

def convert_binary_text_to_np_array(input_text, str_1='#', str_0='.'):
    n_rows = len(input_text)
    n_cols = len(input_text[0])
    for ii in rase(n_rows):
        assert len(input_text[ii]) == n_cols, f'row {ii} has {len(input_text[ii])} cols, not {n_cols}'
        assert all([c in [str_0, str_1] for c in input_text[ii]]), f'row {ii} has invalid characters: {input_text[ii]}'

    return np.array([[1 if c == str_1 else 0 for c in row] for row in input_text])


# for i in {1..25}; do
#   rm -f 2024/day$i/2024_day$i_aoc.ipynb
# done

# for i in {1..25}; do
#   cp template_aoc.ipynb 2024/day$i/2024_day${i}_aoc.ipynb
# done