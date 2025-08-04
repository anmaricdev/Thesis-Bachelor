# Exercise 4: Which Bin? Online Bin Packing
# This script creates exercises where the user has to determine which bin the next item will be placed in using the specified bin packing algorithm.

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

def run_algorithm(algorithm, bin_capacities, items):
    """Helper function to run the specified bin packing algorithm."""
    if algorithm == "BEST":
        return bin_packing_best_fit_var_capa(bin_capacities.copy(), items.copy())
    elif algorithm == "FIRST":
        return bin_packing_first_fit_var_capa(bin_capacities.copy(), items.copy())
    elif algorithm == "NEXT":
        return bin_packing_next_fit_var_capa(bin_capacities.copy(), items.copy())
    elif algorithm == "WORST":
        return bin_packing_worst_fit_var_capa(bin_capacities.copy(), items.copy())
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")

def find_item_placement(bins, target_item, original_items):
    """Helper function to find which bin contains the target item."""
    # Count how many times target_item appears in the original items
    original_count = original_items.count(target_item)
    
    # The new item is the (original_count + 1)th occurrence
    target_occurrence = original_count + 1
    
    # Find the target_occurrence-th occurrence of target_item
    current_occurrence = 0
    for bin_idx, bin_items in enumerate(bins):
        for item in bin_items:
            if item == target_item:
                current_occurrence += 1
                if current_occurrence == target_occurrence:
                    return bin_idx
    return -1

def which_bin_exercise(question_number, num_calls, algorithm):
    # Parameters for random generation
    min_bin_count, max_bin_count = 3, 5
    min_bin_capacity, max_bin_capacity = 6, 14
    min_item_count, max_item_count = 2, 5
    min_item_size, max_item_size = 2, 8
    min_next_item, max_next_item = 2, 6

    arrays = []
    bin_capacities_list = []
    next_items = []
    target_bins = []
    target_bins_regexes = []
    image_filenames = []

    for i in range(num_calls):
        # Generate random bins and items
        bin_count = random.randint(min_bin_count, max_bin_count)
        bin_capacities = [random.randint(min_bin_capacity, max_bin_capacity) for _ in range(bin_count)]
        item_count = random.randint(min_item_count, max_item_count)
        items = [random.randint(min_item_size, max_item_size) for _ in range(item_count)]
        
        # Generate next item that can actually be placed
        next_item = None
        max_attempts = 50  # Prevent infinite loop
        
        for attempt in range(max_attempts):
            candidate_next_item = random.randint(min_next_item, max_next_item)
            
            # Test if this item can be placed
            candidate_items = items + [candidate_next_item]
            is_possible_candidate, bins_candidate, bins_packed_after_failure_candidate = run_algorithm(algorithm, bin_capacities, candidate_items)
            
            # Check if the candidate item was actually placed
            # Count how many times the candidate item appears in the result
            original_count = items.count(candidate_next_item)
            result_count = sum(bin_items.count(candidate_next_item) for bin_items in bins_candidate)
            candidate_item_placed = (result_count > original_count)
            
            if candidate_item_placed:
                next_item = candidate_next_item
                break
        
        # If we couldn't find a placeable item, use a fallback
        if next_item is None:
            next_item = random.randint(min_next_item, max_next_item)

        # Randomize order of bins and items for more variety
        items = copy.deepcopy(items)
        bin_capacities = copy.deepcopy(bin_capacities)
        random.shuffle(items)
        random.shuffle(bin_capacities)

        # Run the algorithm with current items to get the current state
        is_possible, bins, bins_packed_after_failure = run_algorithm(algorithm, bin_capacities, items)

        # Create a list with current items plus the next item
        items_with_next = items + [next_item]
        
        # Run the algorithm with current items + next item to see where it gets placed
        is_possible_with_next, bins_with_next, bins_packed_after_failure_with_next = run_algorithm(algorithm, bin_capacities, items_with_next)
        
        # Find which bin contains the next item
        target_bin = find_item_placement(bins_with_next, next_item, items)

        # Convert to 1-based index for student answer (0 means no bin fits)
        target_bin_1based = target_bin + 1 if target_bin != -1 else 0

        # Generate regex for the target bin
        target_bin_regex = generate_solution_regex(str(target_bin_1based))

        # Save the image (show current state with items, hide solution)
        fig = visualize_bin_packing(
            bin_capacities,
            items,
            visualize_in_2d=False,
            algorithms=[algorithm],
            visualization_options={
                "hide_leftover": True,
                "hide_solution": True,
                "show_items_list": False,
                "hide_bin_filling": False,  # Show current state
                "hide_used_info": False     # Show used info for current state
            }
        )
        image_filename = f"Exercise_{question_number}_{algorithm}_variant_{i+1}.png"
        image_path = os.path.join(folder_path, image_filename)
        fig.savefig(image_path, format='png', bbox_inches='tight', pad_inches=0, dpi=150)
        plt.close(fig)

        arrays.append(items)
        bin_capacities_list.append(bin_capacities)
        next_items.append(next_item)
        target_bins.append(target_bin_1based)
        target_bins_regexes.append(target_bin_regex)
        image_filenames.append(image_filename)

    return [
        (append_question_number_to_string(question_number, 'bin_capacities'), append_question_number_to_string(question_number, 'bin_capacity'), format_list_of_arrays(bin_capacities_list)),
        (append_question_number_to_string(question_number, 'items'), append_question_number_to_string(question_number, 'item'), format_list_of_arrays(arrays)),
        (append_question_number_to_string(question_number, 'next_items'), append_question_number_to_string(question_number, 'next_item'), format_list_of_strings(next_items)),
        (append_question_number_to_string(question_number, 'target_bins'), append_question_number_to_string(question_number, 'target_bin'), format_list_of_strings(target_bins)),
        (append_question_number_to_string(question_number, 'target_bins_regexes'), append_question_number_to_string(question_number, 'target_bin_regex'), format_list_of_strings(target_bins_regexes)),
    ]

# Set the folder where XML and images will be saved
folder_path = r"/Users/antemaric/Desktop/Bachelorarbeit/Thesis-Bachelor/Exercise_4"

clear_variable_declarations(folder_path)

num_calls = 10

algorithms = ["BEST", "FIRST", "NEXT", "WORST"]
for idx, algorithm in enumerate(algorithms, start=1):
    question_number = idx
    result = which_bin_exercise(question_number, num_calls, algorithm)
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