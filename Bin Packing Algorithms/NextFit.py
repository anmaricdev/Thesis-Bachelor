import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import numpy as np

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