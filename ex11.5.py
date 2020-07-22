import bitcoin
import math

from bitcoin.helper import merkle_parent_level

total = 27
max_depth = math.ceil(math.log(total, 2))
merkle_tree = []

for depth in range(max_depth + 1):
    num_items = math.ceil(total / 2**(max_depth - depth))
    level_hashes = [None] * num_items
    merkle_tree.append(level_hashes)

for level in merkle_tree:
    print(level)
