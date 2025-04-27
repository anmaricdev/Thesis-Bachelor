import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import numpy as np

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