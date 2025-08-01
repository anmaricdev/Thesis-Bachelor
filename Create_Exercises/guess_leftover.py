# Exercise 1: Guess the leftover items
# This script creates exercises where the user has to guess the number of leftover items after bin packing.

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
from collections import Counter

def generate_leftover_regex(answer: str) -> str:
    solution = answer
    solution = solution.replace(" ", "").replace(",", r"\s*,\s*").replace("[", r"\[*\s*").replace("]", r"\s*\]*")
    solution = fr"\[*\s*{solution}\s*\]*"
    return f"{solution}"

def guess_leftover_exercise(question_number, num_calls, algorithm):
    # Parameters for random generation
    min_bin_count, max_bin_count = 2, 4
    min_bin_capacity, max_bin_capacity = 6, 12
    min_item_count, max_item_count = 3, 6
    min_item_size, max_item_size = 2, 8

    arrays = []
    bin_capacities_list = []
    leftovers = []
    leftovers_regexes = []
    image_filenames = []
    leftover_items_list = []

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

        # Compute solution using the specified algorithm
        if algorithm == "BEST":
            is_possible, bins, bins_packed_after_failure = bin_packing_best_fit_var_capa(bin_capacities.copy(), items.copy())
        elif algorithm == "FIRST":
            is_possible, bins, bins_packed_after_failure = bin_packing_first_fit_var_capa(bin_capacities.copy(), items.copy())
        elif algorithm == "NEXT":
            is_possible, bins, bins_packed_after_failure = bin_packing_next_fit_var_capa(bin_capacities.copy(), items.copy())
        elif algorithm == "WORST":
            is_possible, bins, bins_packed_after_failure = bin_packing_worst_fit_var_capa(bin_capacities.copy(), items.copy())
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        # Determine leftover items (fixed for duplicates and order)
        packed_items = [item for bin in bins for item in bin]
        
        # Count occurrences in packed items
        packed_counts = Counter(packed_items)
        
        # Calculate leftover items preserving original order
        leftover_items = []
        temp_packed_counts = packed_counts.copy()
        
        for item in items:
            if temp_packed_counts.get(item, 0) > 0:
                # This item was packed, decrement the count
                temp_packed_counts[item] -= 1
            else:
                # This item was not packed, add to leftovers
                leftover_items.append(item)
        
        leftover_count = len(leftover_items)

        # Generate regex for the leftover count
        leftover_regex = generate_leftover_regex(str(leftover_count))

        # Save the image (hide leftover and solution info, but show items list)
        fig = visualize_bin_packing(
            bin_capacities,
            items,
            visualize_in_2d=False,
            algorithms=[algorithm],
            visualization_options={
                "hide_leftover": True,
                "hide_solution": True,
                "show_items_list": True,
                "hide_used_info": True,
                "hide_bin_filling": True
            }
        )
        image_filename = f"Exercise_{question_number}_{algorithm}_variant_{i+1}.png"
        image_path = os.path.join(folder_path, image_filename)
        fig.savefig(image_path, format='png', bbox_inches='tight', pad_inches=0, dpi=150)
        plt.close(fig)
        
          # Solution image creation and saving showing some hidden variables
        fig_solution = visualize_bin_packing(
            bin_capacities,
            items,
            visualize_in_2d=False,
            algorithms=[algorithm],
            visualization_options={
                "hide_leftover": False,
                "hide_solution": True,
                "show_items_list": True,
                "hide_bin_filling": False,
                "hide_used_info": False
            }
        )
        solution_image_filename = f"Solution_{question_number}_{algorithm}_variant_{i+1}.png"
        solution_image_path = os.path.join(folder_path, solution_image_filename)
        fig_solution.savefig(solution_image_path, format='png', bbox_inches='tight', pad_inches=0, dpi=150)
        plt.close(fig_solution)

        arrays.append(items)
        bin_capacities_list.append(bin_capacities)
        leftovers.append(leftover_count)
        leftovers_regexes.append(leftover_regex)
        image_filenames.append(image_filename)
        leftover_items_list.append(leftover_items)

    return [
        (append_question_number_to_string(question_number, 'bin_capacities'), append_question_number_to_string(question_number, 'bin_capacity'), format_list_of_arrays(bin_capacities_list)),
        (append_question_number_to_string(question_number, 'items'), append_question_number_to_string(question_number, 'item'), format_list_of_arrays(arrays)),
        (append_question_number_to_string(question_number, 'leftovers'), append_question_number_to_string(question_number, 'leftover'), format_list_of_strings(leftovers)),
        (append_question_number_to_string(question_number, 'leftover_regexes'), append_question_number_to_string(question_number, 'leftover_regex'), format_list_of_strings(leftovers_regexes)),
        (append_question_number_to_string(question_number, 'leftover_items'), append_question_number_to_string(question_number, 'leftover_item'), format_list_of_arrays(leftover_items_list)),
    ]

# Set the folder where XML and images will be saved
folder_path = r"/Users/antemaric/Desktop/Bachelorarbeit/Thesis-Bachelor/Exercise_1"

clear_variable_declarations(folder_path)

num_calls = 10

# You can loop over all algorithms or specify one
algorithms = ["BEST", "FIRST", "NEXT", "WORST"]
for idx, algorithm in enumerate(algorithms, start=1):
    question_number = idx
    result = guess_leftover_exercise(question_number, num_calls, algorithm)
    exercise_constants = []
    solution_constants = []
    if question_number == 1:
        exercise_constants.append(("image_ids_start", "Put image start id here"))
        solution_constants.append(("solution_image_ids_start", "Put solution image start id here"))
    exercise_constants.append(
        (f"question_{question_number}_image_id", f"[var=image_ids_start] + {str(num_calls*(question_number-1))} + [var=index_question_{question_number}]")
    )
    solution_constants.append(
        (f"question_{question_number}_solution_image_id", f"[var=solution_image_ids_start] + {str(num_calls*(question_number-1))} + [var=index_question_{question_number}]")
    )
    format_to_xml(
        folder_path,
        result,
        question_number,
        num_calls,
        exercise_constants,
        solution_constants
    )