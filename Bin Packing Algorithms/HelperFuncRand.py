import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import numpy as np

np.random.seed(0)

def get_random_capacities_and_items(min_bin_count, max_bin_count, min_bin_capacity, max_bin_capacity, min_item_count, max_item_count, min_item_size, max_item_size, variable_size):
    if min_bin_count > max_bin_count:
        print("Minimum and maximum bin count were implicitly swapped.")
        min_bin_count, max_bin_count = max_bin_count, min_bin_count
    if min_bin_capacity > max_bin_capacity:
        print("Minimum and maximum bin capacity were implicitly swapped.")
        min_bin_capacity, max_bin_capacity = max_bin_capacity, min_bin_capacity
    if min_item_count > max_item_count:
        print("Minimum and maximum item count were implicitly swapped.")
        min_item_count, max_item_count = max_item_count, min_item_count
    if min_item_size > max_item_size:
        print("Minimum and maximum item size were implicitly swapped.")
        min_item_size, max_item_size = max_item_size, min_item_size
    amount_bins = round(np.random.random() *
                     (max_bin_count-min_bin_count) + min_bin_count)
    bin_capacities = []
    for _ in range(amount_bins if variable_size else 1):
        bin_capacity = round(
            np.random.random() * (max_bin_capacity - min_bin_capacity) + min_bin_capacity)
        bin_capacities.append(bin_capacity)
    amount_items = round(np.random.random() *
                     (max_item_count-min_item_count) + min_item_count)
    items = []
    for _ in range(amount_items):
        size = round(np.random.random() *
                     (max_item_size - min_item_size) + min_item_size)
        items.append(size)
    return bin_capacities, items