from BestFit import bin_packing_best_fit_var_capa

# Test case 1: Simple example
bin_capacities = [10, 15, 20]  # Three bins with different capacities
elements = [5, 7, 3, 8, 6, 4]  # Items to pack

success, bins = bin_packing_best_fit_var_capa(bin_capacities, elements)

print("Test Case 1:")
print("Bin capacities:", bin_capacities)
print("Items to pack:", elements)
print("Success:", success)
print("Packed bins:", bins)
print("\nBin details:")
for i, bin_items in enumerate(bins):
    print(f"Bin {i} (capacity {bin_capacities[i]}): {bin_items} - Total: {sum(bin_items)}")

# Test case 2: Items that won't fit
bin_capacities = [5, 5, 5]
elements = [6, 4, 3]  # First item won't fit in any bin

success, bins = bin_packing_best_fit_var_capa(bin_capacities, elements)

print("\nTest Case 2:")
print("Bin capacities:", bin_capacities)
print("Items to pack:", elements)
print("Success:", success)
print("Packed bins:", bins)