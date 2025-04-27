import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import numpy as np

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