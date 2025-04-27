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