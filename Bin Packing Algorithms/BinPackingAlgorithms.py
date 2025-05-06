import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import numpy as np

# First Fit Algorithm
def bin_packing_first_fit_var_capa(bin_capacities, elements):
    m = len(bin_capacities)
    n = len(elements)
    bins = [[] for _ in range(m)]
    for elem in elements:
        i = 0
        found = False
        while i < m and not found:
            if sum(bins[i]) + elem <= bin_capacities[i]:
                found = True
            else:
                i += 1
        if found:
            bins[i] += [elem]
        else:
            return found, bins
    return found, bins

def bin_packing_first_fit_fixed_capa(bin_capacity, m, elements):
    return bin_packing_first_fit_var_capa([bin_capacity] * m, elements)

# Next Fit Algorithm
def bin_packing_next_fit_var_capa(bin_capacities, elements):
    m = len(bin_capacities)
    n = len(elements)
    bins = [[] for _ in range(m)]
    current_bin = 0
    for elem in elements:
        while current_bin < m and \
                sum(bins[current_bin]) + elem > bin_capacities[current_bin]:
            current_bin += 1
        if current_bin < m:
            bins[current_bin] += [elem]
        else:
            return False, bins
    return True, bins


# Best Fit Algorithm
def bin_packing_best_fit_var_capa(bin_capacities, elements):
    max_capacity = max(bin_capacities)
    m = len(bin_capacities)
    n = len(elements)
    bins = [[] for _ in range(m)]
    bins_in_use = [i for i in range(m)]
    for elem in elements:
        # search for bin in use where it fits best
        best_bin = -1
        best_remaining_capacity = max_capacity + 1
        for i in range(len(bins_in_use)):
            remaining_capacity = bin_capacities[bins_in_use[i]
                                                ] - (sum(bins[bins_in_use[i]]) + elem)
            if remaining_capacity >= 0 and \
               remaining_capacity < best_remaining_capacity:
                best_bin = bins_in_use[i]
                best_remaining_capacity = remaining_capacity
        # found?
        if best_bin != -1:
            bins[best_bin] += [elem]
            # is this bin full now?
            if best_remaining_capacity == 0:
                bins_in_use.remove(best_bin)
        else:
            return False, bins
    return True, bins

# Worst Fit Algorithm
def bin_packing_worst_fit_var_capa(bin_capacities, elements):
    max_capacity = max(bin_capacities)
    m = len(bin_capacities)
    n = len(elements)
    bins = [[] for _ in range(m)]
    bins_in_use = [i for i in range(m)]
    for elem in elements:
        # search for bin in use where it fits worst
        worst_bin = -1
        worst_remaining_capacity = -1
        for i in range(len(bins_in_use)):
            remaining_capacity = bin_capacities[bins_in_use[i]
                                                ] - (sum(bins[bins_in_use[i]]) + elem)
            if remaining_capacity >= 0 and \
               remaining_capacity > worst_remaining_capacity:
                worst_bin = bins_in_use[i]
                worst_remaining_capacity = remaining_capacity
        # found?
        if worst_bin != -1:
            bins[worst_bin] += [elem]
            # is this bin full now?
            if worst_remaining_capacity == 0:
                bins_in_use.remove(worst_bin)
        else:
            return False, bins
    return True, bins