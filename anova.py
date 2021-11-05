import getopt
import sys
import numpy as np
from itertools import cycle
import pandas as pd

from numpy.lib.ufunclike import fix


fixed = []
random = []
crossed = []
nested = []
residual = []
letters = "H I J K L M".split(" ")

def check_reserved(input):
    for l in letters:
        if l in input:
            raise Exception(f"Reserved character: {l}")

def get_arguments():
    options, arguments = getopt.getopt(
            sys.argv[1:],                      # Arguments
            'f:r:c:n:e:',                            # Short option definitions
            ["fixed=", "random=", "crossed=", "nested=", "residual="])                # Long option definitions
    fixed = []
    random = []
    crossed = []
    nested = []
    residual = []
    for o, a in options:
        if o in ('-f', '--fixed'):
            fixed = a.split(" ")
            check_reserved(fixed)
            print(f'Fixed params: {fixed}')
        if o in ('-r', '--random'):
            random = a.split(" ")
            check_reserved(random)
            print(f'Random params: {random}')
        if o in ('-c', '--crossed'):
            crossed = a.split(" ")
            check_reserved(crossed)
            print(f'Crossed params: {crossed}')
        if o in ('-n', '--nested'):
            nested = a.split(" ")
            check_reserved(nested)
            print(f'Nested params: {nested}')
        if o in ('-e', '--residual'):
            residual = a.split(" ")
            check_reserved(residual)
            print(f'Residual params: {residual}')
        
    return fixed, random, crossed, nested, residual
        

def create_index():
    index = fixed.copy()
    index.extend(random)
    index.extend(crossed)
    index.extend(nested)
    index.extend(residual)
    return index

fixed, random, crossed, nested, residual = get_arguments()
index = create_index()
n = len(index)
matrix = np.array([ n*["0"] for _ in range(n)], dtype=object)
for i in range(n):
    matrix[i,i] = "X"
for i in range(n):
    for j in range(i, n):
        is_in = True
        for el in index[i]:
            if el not in index[j]:
                is_in = False
        matrix[i,j] = "X" if is_in else "0"

matrix[:,-1] = n*["1"]
# print(matrix)

l_for_i = {}
letter_cycle = cycle(letters)

for idx in index:
    for L in idx:
        if L.isalnum() and all([L not in k for k in l_for_i.keys()]):
            l_for_i[L] = next(letter_cycle)

# print("\n")
for j in range(n):
    missing = ""
    for idx in l_for_i.keys():
        if idx not in index[j]:
            missing += l_for_i[idx]
    # print(f"Missing: {missing}")
    for i in range(0, j+1):
        if matrix[i,j] == 'X':
            matrix[i,j] = missing


# print(index)
# print(matrix)        

# Add letters
degrees_of_freedom = n * [""]
for i, idx in enumerate(index):
    parts = idx.split('(')
    if len(parts) == 1:
        # No nested
        for L in parts[0]:
            degrees_of_freedom[i] += f"({l_for_i[L]}-1)"
    elif len(parts) > 1:
        not_nested = parts[0]
        nested = parts[1].split(')')[0]
        for L in nested:
            degrees_of_freedom[i] += f"{l_for_i[L]}"
        for L in not_nested:
            degrees_of_freedom[i] += f"({l_for_i[L]}-1)"


# print(degrees_of_freedom)

# delete fixed vc-s

for j, idx in enumerate(index):
    is_only_fixed = True
    for L in idx:
        if L not in fixed:
            is_only_fixed = False
    if is_only_fixed: 
        for i in range (0, j):
            matrix[i, j] = "0"

# print(index)
# print(matrix)        


# Get letters for all indices
l_for_i_all = {}
letters_for_all = n*[""]
letter_cycle = cycle(letters)

for i, idx in enumerate(index):
    new = False
    lettr = ""
    for L in idx:
        if L.isalnum() and all([L not in k for k in l_for_i_all.keys()]):
            l_for_i_all[L] = next(letter_cycle)
            new = True
            lettr = l_for_i_all[L]
    if new:
        letters_for_all[i] = lettr

# Calculate sums of squares 
for i, idx in enumerate(index):
    missing = matrix[i,i]
    d_f = degrees_of_freedom[i]











# PRINT
df = pd.DataFrame(data=matrix, columns=index)
df["Degrees of Freedom"] = degrees_of_freedom
df.insert(0, column="index", value=index)
df.insert(0, column="letter", value=letters_for_all)

print("\n\n", df)

