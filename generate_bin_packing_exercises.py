import os
from datetime import datetime
from Bin_Packing_Algorithms.HelperFuncRand import get_random_capacities_and_items
from Bin_Packing_Algorithms.Visualization import visualize_bin_packing
from Bin_Packing_Algorithms.BinPackingAlgorithms import (
    bin_packing_best_fit_var_capa,
    bin_packing_first_fit_var_capa,
    bin_packing_next_fit_var_capa,
    bin_packing_worst_fit_var_capa
)

# PARAMETERS (adjust as needed)
AMOUNT_ITERATIONS = 10
BINS_COUNT_MIN = 3
BINS_COUNT_MAX = 5
BINS_CAPACITY_MIN = 8
BINS_CAPACITY_MAX = 15
ITEM_COUNT_MIN = 8
ITEM_COUNT_MAX = 12
ITEM_SIZE_MIN = 1
ITEM_SIZE_MAX = 8
ALLOW_VARIABLE_SIZE = True
ALGORITHM = "BEST"  # or "FIRST", "NEXT", "WORST"

# Output folder
folder_path = os.path.join(os.path.dirname(__file__), "Generated Pictures")
os.makedirs(folder_path, exist_ok=True)

# Algorithm mapping
algo_map = {
    "BEST": bin_packing_best_fit_var_capa,
    "FIRST": bin_packing_first_fit_var_capa,
    "NEXT": bin_packing_next_fit_var_capa,
    "WORST": bin_packing_worst_fit_var_capa
}

for i in range(AMOUNT_ITERATIONS):
    # Generate random task
    capacities, items = get_random_capacities_and_items(
        BINS_COUNT_MIN, BINS_COUNT_MAX,
        BINS_CAPACITY_MIN, BINS_CAPACITY_MAX,
        ITEM_COUNT_MIN, ITEM_COUNT_MAX,
        ITEM_SIZE_MIN, ITEM_SIZE_MAX,
        ALLOW_VARIABLE_SIZE
    )

    # Visualize and save
    fig = visualize_bin_packing(capacities, items, visualize_in_2d=False, algorithms=[ALGORITHM])
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    save_path = os.path.join(folder_path, f"{timestamp_str}.png")
    fig.savefig(save_path, format='png', bbox_inches='tight', pad_inches=0, dpi=300, transparent=False)
    print(f"Saved: {save_path}")
    fig.clf() 