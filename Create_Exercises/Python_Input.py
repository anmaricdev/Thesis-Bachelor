# First Fit Algorithm #######################################
def bin_packing_first_fit_var_capa(bin_capacities, elements):
    is_packing_possible = True
    n = len(elements)
    m = len(bin_capacities)
    bins = [[] for _ in range(m)]
    bins_packed_after_failure = [[] for _ in range(m)]
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
            if not is_packing_possible:
                bins_packed_after_failure[i] += [elem]
        else:
            is_packing_possible = False
    return is_packing_possible, bins, bins_packed_after_failure

def bin_packing_first_fit_fixed_capa(bin_capacity, m, elements):
    return bin_packing_first_fit_var_capa([bin_capacity] * m, elements)


# Next Fit Algorithm #######################################
def bin_packing_next_fit_fixed_capa(bin_capacity, m, elements):
    is_packing_possible = True
    n = len(elements)
    bins = [[] for _ in range(m)]
    bins_packed_after_failure = [[] for _ in range(m)]
    current_bin = 0
    for elem in elements:
        if sum(bins[current_bin]) + elem <= bin_capacity:
            bins[current_bin] += [elem]
            if not is_packing_possible:
                bins_packed_after_failure[current_bin] += [elem]
        else:
            current_bin += 1
            if current_bin < m and \
               sum(bins[current_bin]) + elem <= bin_capacity:
                bins[current_bin] += [elem]
                if not is_packing_possible:
                    bins_packed_after_failure[current_bin] += [elem]
            else:
                is_packing_possible = False
    return is_packing_possible, bins, bins_packed_after_failure

def bin_packing_next_fit_var_capa(bin_capacities, elements):
    is_packing_possible = True
    n = len(elements)
    m = len(bin_capacities)
    bins = [[] for _ in range(m)]
    bins_packed_after_failure = [[] for _ in range(m)]
    current_bin = 0
    for elem in elements:
        while current_bin < m and \
                sum(bins[current_bin]) + elem > bin_capacities[current_bin]:
            current_bin += 1
        if current_bin < m:
            bins[current_bin] += [elem]
            if not is_packing_possible:
                bins_packed_after_failure[current_bin] += [elem]
        else:
            is_packing_possible = False
    return is_packing_possible, bins, bins_packed_after_failure


# Best Fit Algorithm #######################################
def bin_packing_best_fit_fixed_capa(bin_capacity, m, elements):
    is_packing_possible = True
    n = len(elements)
    bins = [[] for _ in range(m)]
    bins_in_use = []
    bins_packed_after_failure = [[] for _ in range(m)]
    last_added_bin = -1
    for elem in elements:
        # search for bin in use where it fits best
        best_bin = -1
        best_remaining_capacity = bin_capacity
        for b in bins_in_use:
            remaining_capacity = bin_capacity - (sum(bins[b]) + elem)
            if remaining_capacity >= 0 and \
               remaining_capacity < best_remaining_capacity:
                best_bin = b
                best_remaining_capacity = remaining_capacity
        # if not found: add new bin, if possible
        if best_bin == -1 and last_added_bin < m-1:
            last_added_bin += 1
            bins_in_use += [last_added_bin]
            remaining_capacity = bin_capacity - elem
            if remaining_capacity >= 0:
                best_bin = last_added_bin
                best_remaining_capacity = remaining_capacity
        # found? - if not: new bin - does it fit there?
        if best_bin != -1:
            bins[best_bin] += [elem]
            if not is_packing_possible:
                bins_packed_after_failure[best_bin] += [elem]
            # is this bin full now?
            if best_remaining_capacity == 0:
                bins_in_use.remove(best_bin)
        else:
            is_packing_possible = False
    return is_packing_possible, bins, bins_packed_after_failure

def bin_packing_best_fit_var_capa(bin_capacities, elements):
    is_packing_possible = True
    n = len(elements)
    m = len(bin_capacities)
    max_capacity = max(bin_capacities)
    bins = [[] for _ in range(m)]
    bins_in_use = [i for i in range(m)]
    bins_packed_after_failure = [[] for _ in range(m)]
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
            if not is_packing_possible:
                bins_packed_after_failure[best_bin] += [elem]
            # is this bin full now?
            if best_remaining_capacity == 0:
                bins_in_use.remove(best_bin)
        else:
            is_packing_possible = False
    return is_packing_possible, bins, bins_packed_after_failure


# Worst Fit Algorithm #######################################
def bin_packing_worst_fit_fixed_capa(bin_capacity, m, elements):
    is_packing_possible = True
    n = len(elements)
    bins = [[] for _ in range(m)]
    bins_in_use = [i for i in range(m)]
    bins_packed_after_failure = [[] for _ in range(m)]
    for elem in elements:
        # search for bin in use where it fits worst
        worst_bin = -1
        worst_remaining_capacity = -1
        for b in bins_in_use:
            remaining_capacity = bin_capacity - (sum(bins[b]) + elem)
            if remaining_capacity >= 0 and \
               remaining_capacity > worst_remaining_capacity:
                worst_bin = b
                worst_remaining_capacity = remaining_capacity
        # found?
        if worst_bin != -1:
            bins[worst_bin] += [elem]
            if not is_packing_possible:
                bins_packed_after_failure[worst_bin] += [elem]
            # is this bin full now?
            if worst_remaining_capacity == 0:
                bins_in_use.remove(worst_bin)
        else:
            is_packing_possible = False
    return is_packing_possible, bins, bins_packed_after_failure

def bin_packing_worst_fit_var_capa(bin_capacities, elements):
    is_packing_possible = True
    n = len(elements)
    m = len(bin_capacities)
    max_capacity = max(bin_capacities)
    bins = [[] for _ in range(m)]
    bins_in_use = [i for i in range(m)]
    bins_packed_after_failure = [[] for _ in range(m)]
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
            if not is_packing_possible:
                bins_packed_after_failure[worst_bin] += [elem]
            # is this bin full now?
            if worst_remaining_capacity == 0:
                bins_in_use.remove(worst_bin)
        else:
            is_packing_possible = False
    return is_packing_possible, bins, bins_packed_after_failure