# Exercise 2: Order of Placement
# This script creates exercises where the user has to specify the order in which items are placed into bins using the various Bin packing algorithms.

import random
from formatter_for_copy_paste_export_to_jack3 import *
from formatter_to_xml import format_to_xml, clear_variable_declarations
from append_question_number_to_string import append_question_number_to_string
import matplotlib.pyplot as plt
from Visualization import visualize_bin_packing
from BinPackingAlgorithms import (
    bin_packing_best_fit_var_capa,
    bin_packing_first_fit_var_capa,
    bin_packing_next_fit_var_capa,
    bin_packing_worst_fit_var_capa
)
import os
import copy

def generate_solution_regex(answer: str) -> str:
    solution = answer
    solution = solution.replace(" ", "").replace(",", r"\s*,\s*").replace("[", r"\[*\s*").replace("]", r"\s*\]*")
    solution = fr"\[*\s*{solution}\s*\]*"
    return f"{solution}"

def order_of_placement_exercise(question_number, num_calls, algorithm):
    # Parameters for random generation
    min_bin_count, max_bin_count = 2, 5
    min_bin_capacity, max_bin_capacity = 4, 15
    min_item_count, max_item_count = 3, 9
    min_item_size, max_item_size = 1, 12

    arrays = []
    bin_capacities_list = []
    placements = []
    placements_regexes = []
    image_filenames = []

    for i in range(num_calls):
        # Generate random bins and items
        bin_count = random.randint(min_bin_count, max_bin_count)
        bin_capacities = [random.randint(min_bin_capacity, max_bin_capacity) for _ in range(bin_count)]
        item_count = random.randint(min_item_count, max_item_count)
        items = [random.randint(min_item_size, max_item_size) for _ in range(item_count)]

        # Randomize order of bins and items for more variety
        items = copy.deepcopy(items)
        bin_capacities = copy.deepcopy(bin_capacities)
        random.shuffle(items)
        random.shuffle(bin_capacities)

        # Track the order of placement for each item (1-based bin indices)
        # We need to simulate the algorithm step by step using professor's algorithms
        placement_order = []
        
        # Simulate each step by running the algorithm with progressively more items
        for step in range(1, len(items) + 1):
            # Run algorithm with first 'step' items
            current_items = items[:step]
            
            # Call the appropriate algorithm function
            if algorithm == "BEST":
                is_possible, bins, bins_packed_after_failure = bin_packing_best_fit_var_capa(bin_capacities.copy(), current_items)
            elif algorithm == "FIRST":
                is_possible, bins, bins_packed_after_failure = bin_packing_first_fit_var_capa(bin_capacities.copy(), current_items)
            elif algorithm == "NEXT":
                is_possible, bins, bins_packed_after_failure = bin_packing_next_fit_var_capa(bin_capacities.copy(), current_items)
            elif algorithm == "WORST":
                is_possible, bins, bins_packed_after_failure = bin_packing_worst_fit_var_capa(bin_capacities.copy(), current_items)
            else:
                raise ValueError(f"Unknown algorithm: {algorithm}")
            
            # Find which bin the current item was placed in
            current_item = items[step - 1]  # The item we just added
            
            # Find the bin that contains this item
            placed_bin = -1
            for bin_idx, bin_items in enumerate(bins):
                if current_item in bin_items:
                    placed_bin = bin_idx
                    break
            
            if placed_bin != -1:
                placement_order.append(placed_bin + 1)  # 1-based index
            else:
                placement_order.append(0)  # 0 means not placed

        # Generate regex for the placement order
        placement_str = ",".join(map(str, placement_order))
        placement_regex = generate_solution_regex(placement_str)

        # Save the image (show items list, hide solution info)
        fig = visualize_bin_packing(
            bin_capacities,
            items,
            visualize_in_2d=False,
            algorithms=[algorithm],
            visualization_options={
                "hide_leftover": True,
                "hide_solution": True,
                "show_items_list": True
            }
        )
        image_filename = f"Exercise_{question_number}_{algorithm}_variant_{i+1}.png"
        image_path = os.path.join(folder_path, image_filename)
        fig.savefig(image_path, format='png', bbox_inches='tight', pad_inches=0, dpi=150)
        plt.close(fig)

        arrays.append(items)
        bin_capacities_list.append(bin_capacities)
        placements.append(placement_order)
        placements_regexes.append(placement_regex)
        image_filenames.append(image_filename)

    return [
        (append_question_number_to_string(question_number, 'bin_capacities'), append_question_number_to_string(question_number, 'bin_capacity'), format_list_of_arrays(bin_capacities_list)),
        (append_question_number_to_string(question_number, 'items'), append_question_number_to_string(question_number, 'item'), format_list_of_arrays(arrays)),
        (append_question_number_to_string(question_number, 'placements'), append_question_number_to_string(question_number, 'placement'), format_list_of_arrays(placements)),
        (append_question_number_to_string(question_number, 'placements_regexes'), append_question_number_to_string(question_number, 'placement_regex'), format_list_of_strings(placements_regexes)),
    ]

# Set the folder where XML and images will be saved
folder_path = r"/Users/antemaric/Desktop/Bachelorarbeit/Thesis-Bachelor/Exercise_2"

clear_variable_declarations(folder_path)

num_calls = 10

algorithms = ["BEST", "FIRST", "NEXT", "WORST"]
for idx, algorithm in enumerate(algorithms, start=1):
    question_number = idx
    result = order_of_placement_exercise(question_number, num_calls, algorithm)
    exercise_constants = []
    if question_number == 1:
        exercise_constants.append(("image_ids_start", "Put image start id here"))
    exercise_constants.append(
        (f"question_{question_number}_image_id", f"[var=image_ids_start] + {str(num_calls*(question_number-1))} + [var=index_question_{question_number}]")
    )
    format_to_xml(
        folder_path,
        result,
        question_number,
        num_calls,
        exercise_constants
    )
