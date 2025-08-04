from BinPackingAlgorithms import bin_packing_best_fit_var_capa
from Class_Items import create_items_bulk

# Test the specific case
items = [2, 7, 2, 6, 3]
capacities = [11, 11, 8]

print(f"Original items: {items}")
print(f"Capacities: {capacities}")

# Create item objects
items_obj = create_items_bulk(*items)
print(f"Item objects: {items_obj}")

# Check if the order is preserved
print(f"\nChecking order preservation:")
for i, (original_item, item_obj) in enumerate(zip(items, items_obj)):
    print(f"Original[{i}]: {original_item}, Item object[{i}]: {item_obj.size}")

# Run Best Fit
is_possible, used_bins, bins_packed_after_failure = bin_packing_best_fit_var_capa(capacities.copy(), items_obj)

print(f"\nAlgorithm result:")
for i, bin_items in enumerate(used_bins):
    print(f"Bin {i+1}: {[item.size for item in bin_items]}")

# Now let's trace the placement order
print(f"\nPlacement order:")
placed_items_in_order = []
for bin_items in used_bins:
    for item in bin_items:
        placed_items_in_order.append((item.size, item))

for i, (size, item) in enumerate(placed_items_in_order):
    print(f"Item {i+1}: size {size}, object {item}")

# Now let's match original items to placement order
print(f"\nMatching original items to placement:")
matched_items = set()

for i, original_item in enumerate(items):
    print(f"\nOriginal item {i+1}: size {original_item}")
    
    # Find the first unmatched item with the same size
    found = False
    for j, (placed_size, placed_item) in enumerate(placed_items_in_order):
        if placed_size == original_item and placed_item not in matched_items:
            # Find which bin this item is in
            for bin_idx, bin_items in enumerate(used_bins):
                if placed_item in bin_items:
                    print(f"  → Matches placed item {j+1} (size {placed_size}) in bin {bin_idx+1}")
                    matched_items.add(placed_item)
                    found = True
                    break
            if found:
                break
    
    if not found:
        print(f"  → No match found!")

# Now let's generate the correct bin hints
print(f"\nCorrect bin hints:")
items_text_parts = []
items_text_parts.append("Items to pack:\n [")

matched_items = set()

for i, item in enumerate(items):
    # Find the corresponding item object in placed_items_in_order that hasn't been matched yet
    item_obj = None
    bin_number = None
    
    # Look for the first unmatched item with the same size
    for placed_size, placed_item in placed_items_in_order:
        if placed_size == item and placed_item not in matched_items:
            # Find which bin this item is in
            for bin_idx, bin_items in enumerate(used_bins):
                if placed_item in bin_items:
                    item_obj = placed_item
                    bin_number = bin_idx + 1  # 1-based bin numbering
                    matched_items.add(placed_item)
                    break
            if item_obj:
                break
    
    # Add the item with bin hint if it's a duplicate
    if bin_number:
        # Check if this item appears multiple times
        item_count = items.count(item)
        if item_count > 1:
            items_text_parts.append(f"{item} (bin{bin_number})")
        else:
            items_text_parts.append(str(item))
    else:
        items_text_parts.append(str(item))
    
    # Add comma separator (except for last item)
    if i < len(items) - 1:
        items_text_parts.append(", ")

items_text_parts.append("]")
items_text = "".join(items_text_parts)
print(items_text)

# Now let's trace through the algorithm manually
print(f"\nManual trace of Best Fit algorithm:")
bins = [[], [], []]
bins_in_use = [0, 1, 2]
capacities_copy = capacities.copy()

for i, elem in enumerate(items_obj):
    print(f"\nPlacing item {i+1}: size {elem.size}")
    
    # Find best bin
    best_bin = -1
    best_remaining_capacity = max(capacities) + 1
    
    for bin_idx in bins_in_use:
        remaining_capacity = capacities_copy[bin_idx] - (sum(bins[bin_idx]) + elem.size)
        print(f"  Bin {bin_idx+1}: capacity {capacities_copy[bin_idx]}, used {sum(bins[bin_idx])}, remaining after placement {remaining_capacity}")
        if remaining_capacity >= 0 and remaining_capacity < best_remaining_capacity:
            best_bin = bin_idx
            best_remaining_capacity = remaining_capacity
    
    print(f"  Best bin: {best_bin+1} (remaining capacity: {best_remaining_capacity})")
    bins[best_bin].append(elem.size)
    print(f"  Result: {bins}") 