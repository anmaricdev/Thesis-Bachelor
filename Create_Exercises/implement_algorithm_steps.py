# Exercise 3: Step-by-Step Algorithm Implementation (Remaining capacities)
# This script creates exercises where the user has to simulate the bin packing algorithm step by step, entering the bin states after each item is placed.

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

def step_by_step_simulation_exercise(question_number, num_calls, algorithm):
    # Parameters for random generation
    min_bin_count, max_bin_count = 2, 4
    min_bin_capacity, max_bin_capacity = 6, 12
    min_item_count, max_item_count = 3, 6
    min_item_size, max_item_size = 2, 8

    arrays = []
    bin_capacities_list = []
    step_states = []
    step_states_regexes = []

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

        # Simulate the algorithm step by step using the Bin Packing algorithms
        step_states_for_variant = []
        
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
            
            # Calculate remaining capacities after this step
            remaining_capacities = []
            for bin_idx in range(len(bin_capacities)):
                used_capacity = sum(bins[bin_idx])
                remaining = bin_capacities[bin_idx] - used_capacity
                remaining_capacities.append(remaining)
            
            step_states_for_variant.append(remaining_capacities)

        # Generate regex for the step states
        step_states_str = str(step_states_for_variant)
        step_states_regex = generate_solution_regex(step_states_str)

        # Save the EXERCISE image (hide filling, used info, and solution)
        fig_exercise = visualize_bin_packing(
            bin_capacities,
            items,
            visualize_in_2d=False,
            algorithms=[algorithm],
            visualization_options={
                "hide_leftover": True,
                "hide_solution": True,
                "show_items_list": True,
                "hide_bin_filling": True,
                "hide_used_info": True
            }
        )
        exercise_image_filename = f"Exercise_{question_number}_{algorithm}_variant_{i+1}.png"
        exercise_image_path = os.path.join(folder_path, exercise_image_filename)
        fig_exercise.savefig(exercise_image_path, format='png', bbox_inches='tight', pad_inches=0, dpi=150)
        plt.close(fig_exercise)

        # Save the SOLUTION image (show everything for feedback)
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
        step_states.append(step_states_for_variant)
        step_states_regexes.append(step_states_regex)

    return [
        (append_question_number_to_string(question_number, 'bin_capacities'), append_question_number_to_string(question_number, 'bin_capacity'), format_list_of_arrays(bin_capacities_list)),
        (append_question_number_to_string(question_number, 'items'), append_question_number_to_string(question_number, 'item'), format_list_of_arrays(arrays)),
        (append_question_number_to_string(question_number, 'step_states'), append_question_number_to_string(question_number, 'step_state'), format_list_of_arrays(step_states)),
        (append_question_number_to_string(question_number, 'step_states_regexes'), append_question_number_to_string(question_number, 'step_state_regex'), format_list_of_strings(step_states_regexes)),
    ]

# Set the folder where XML and images will be saved
folder_path = r"/Users/antemaric/Desktop/Bachelorarbeit/Thesis-Bachelor/Exercise_3"

clear_variable_declarations(folder_path)

num_calls = 10

algorithms = ["BEST", "FIRST", "NEXT", "WORST"]
for idx, algorithm in enumerate(algorithms, start=1):
    question_number = idx
    result = step_by_step_simulation_exercise(question_number, num_calls, algorithm)
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