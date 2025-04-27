from Visualization import visualize_bin_packing
from Item import create_items_bulk

# Test case 1: Different bin sizes with successful packing
bin_capacities = [8, 12, 15, 20]
items = [5, 7, 3, 8, 6, 4, 2, 9]

print("Test Case 1: Different bin sizes with successful packing")
visualize_bin_packing(bin_capacities, items)

# Test case 2: Unsuccessful packing with leftovers
bin_capacities = [10, 10, 10]
items = [12, 8, 6, 5, 4]  # First item won't fit in any bin

print("\nTest Case 2: Unsuccessful packing with leftovers")
visualize_bin_packing(bin_capacities, items)

# Test case 3: Mixed success with some bins too small
bin_capacities = [5, 8, 12, 15]
items = [6, 4, 7, 3, 5, 8]  # First item won't fit in first bin

print("\nTest Case 3: Mixed success with some bins too small")
visualize_bin_packing(bin_capacities, items)

# Test case 4: Large bins with small items
bin_capacities = [25, 30, 35]
items = [3, 4, 5, 6, 7, 8, 9, 10]

print("\nTest Case 4: Large bins with small items")
visualize_bin_packing(bin_capacities, items) 