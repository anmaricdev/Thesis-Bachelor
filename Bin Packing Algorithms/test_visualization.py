from Visualization import visualize_bin_packing
from Item import create_items_bulk
from HelperFuncRand import get_random_capacities_and_items

AMOUNT_ITERATIONS = 2
ALLOW_VARIABLE_SIZE = True

BINS_COUNT_MIN = 3
BINS_COUNT_MAX = 5
BINS_CAPACITY_MIN = 5
BINS_CAPACITY_MAX = 12
ITEM_COUNT_MIN = 3
ITEM_COUNT_MAX = 5
ITEM_SIZE_MIN = 1
ITEM_SIZE_MAX = 10

for _ in range(AMOUNT_ITERATIONS):
    capacities, items = get_random_capacities_and_items(
        BINS_COUNT_MIN, BINS_COUNT_MAX, BINS_CAPACITY_MIN, BINS_CAPACITY_MAX, ITEM_COUNT_MIN, ITEM_COUNT_MAX, ITEM_SIZE_MIN, ITEM_SIZE_MAX, ALLOW_VARIABLE_SIZE)
    print("capacities =", capacities)
    print("items =", items)
    visualize_bin_packing(capacities, items)