# Exercise 5: Guess the Algorithm
# This script creates exercises where the user has to determine which bin packing algorithm was used based on the final packed state.

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

def guess_algorithm_exercise(question_number, num_calls):
    # Parameters for random generation
    min_bin_count, max_bin_count = 2, 4
    min_bin_capacity, max_bin_capacity = 6, 12
    min_item_count, max_item_count = 3, 6
    min_item_size, max_item_size = 2, 8

    arrays = []
    bin_capacities_list = []
    correct_algorithms = []
    image_filenames = []

    # Algorithm mapping for student input (0-based indexing)
    algorithm_mapping = {
        "BEST": 0,
        "FIRST": 1, 
        "NEXT": 2,
        "WORST": 3
    }

    attempts = 0
    max_attempts = 100  # Prevent infinite loops
    successful_variant_count = 0  # Track successful variants separately
    
    for i in range(num_calls):
        attempts = 0
        valid_scenario_found = False
        
        while attempts < max_attempts and not valid_scenario_found:
            attempts += 1
            
            # Generate random bins and items
            bin_count = random.randint(min_bin_count, max_bin_count)
            bin_capacities = [random.randint(min_bin_capacity, max_bin_capacity) for _ in range(bin_count)]
            item_count = random.randint(min_item_count, max_item_count)
            items = [random.randint(min_item_size, max_item_size) for _ in range(item_count)]

            # Randomize order of bins and items for more variety
            shuffled_items = copy.deepcopy(items)
            shuffled_bin_capacities = copy.deepcopy(bin_capacities)
            random.shuffle(shuffled_items)
            random.shuffle(shuffled_bin_capacities)

            # Randomly select one algorithm to use for this variant
            selected_algorithm = random.choice(["BEST", "FIRST", "NEXT", "WORST"])
            
            # Run the selected algorithm to get the target result
            is_possible, target_bins, bins_packed_after_failure = run_algorithm(selected_algorithm, shuffled_bin_capacities, shuffled_items)
            
            # Test all algorithms to see if only the selected one produces this result
            algorithm_results = {}
            unique_result = True
            
            for test_algorithm in ["BEST", "FIRST", "NEXT", "WORST"]:
                test_is_possible, test_bins, test_bins_packed_after_failure = run_algorithm(test_algorithm, shuffled_bin_capacities, shuffled_items)
                algorithm_results[test_algorithm] = test_bins
                
                # Check if any other algorithm produces the same result
                # Convert bin contents to lists of item sizes for proper comparison
                # Handle both item objects and integers
                def get_bin_sizes(bins):
                    result = []
                    for bin_items in bins:
                        if isinstance(bin_items, list):
                            if len(bin_items) > 0 and hasattr(bin_items[0], 'size'):
                                # Item objects
                                result.append([item.size for item in bin_items])
                            else:
                                # Integers
                                result.append(bin_items)
                        else:
                            result.append([])
                    return result
                
                target_bin_sizes = get_bin_sizes(target_bins)
                test_bin_sizes = get_bin_sizes(test_bins)
                
                if test_algorithm != selected_algorithm and test_bin_sizes == target_bin_sizes:
                    unique_result = False
                    print(f"  {test_algorithm} produces same result as {selected_algorithm}")
                    break
            
            if unique_result:
                valid_scenario_found = True
                print(f"Variant {i+1}: Found unique scenario for {selected_algorithm} after {attempts} attempts")
                print(f"  Target result: {target_bins}")
                for alg, result in algorithm_results.items():
                    print(f"  {alg}: {result}")
                print(f"  Correct answer should be: {algorithm_mapping[selected_algorithm]} ({selected_algorithm})")
            else:
                print(f"Variant {i+1}: Attempt {attempts} - multiple algorithms produce same result, retrying...")
                print(f"  Target result: {target_bins}")
                for alg, result in algorithm_results.items():
                    print(f"  {alg}: {result}")

        # Only process the scenario if we found a valid one
        if valid_scenario_found:
            # Convert algorithm to student answer number (integer)
            correct_algorithm_number = algorithm_mapping[selected_algorithm]

            # Save the image (show final state with solution, but hide which algorithm was used)
            fig = visualize_bin_packing(
                shuffled_bin_capacities,
                shuffled_items,  # Use shuffled items for algorithm calculation
                visualize_in_2d=False,
                algorithms=[selected_algorithm],  # This will show the final state
                visualization_options={
                    "hide_leftover": True,
                    "hide_solution": True,  # Show the final packed state
                    "show_items_list": True,  # Show the items list for reference
                    "hide_bin_filling": False,  # Show how bins are filled
                    "hide_used_info": False,     # Show used info
                    "hide_algorithm_name": True,  # Hide the algorithm name
                    "show_placement_order": True  # Show placement order indicators
                }
            )
            successful_variant_count += 1
            image_filename = f"variant_{successful_variant_count:02d}_Exercise_{question_number}_{selected_algorithm}.png"
            image_path = os.path.join(folder_path, image_filename)
            fig.savefig(image_path, format='png', bbox_inches='tight', pad_inches=0, dpi=150)
            plt.close(fig)

            # Store the same items array that was used for the algorithm
            arrays.append(shuffled_items)
            bin_capacities_list.append(shuffled_bin_capacities)
            correct_algorithms.append(correct_algorithm_number)
            image_filenames.append(image_filename)
            print(f"  SAVED: Variant {len(arrays)} with algorithm {selected_algorithm} (index {correct_algorithm_number})")
            print(f"    Items: {shuffled_items}")
            print(f"    Bin capacities: {shuffled_bin_capacities}")
        else:
            print(f"Variant {i+1}: Could not find unique scenario after {max_attempts} attempts, skipping...")

    # Debug: Print the final correct_algorithms list
    print("\nFINAL CORRECT ALGORITHMS LIST:")
    for i, alg_idx in enumerate(correct_algorithms):
        alg_name = {0: "BEST", 1: "FIRST", 2: "NEXT", 3: "WORST"}[alg_idx]
        print(f"  Saved Variant {i+1}: {alg_name} (index {alg_idx})")
    
    return [
        (append_question_number_to_string(question_number, 'bin_capacities'), append_question_number_to_string(question_number, 'bin_capacity'), format_list_of_arrays(bin_capacities_list)),
        (append_question_number_to_string(question_number, 'items'), append_question_number_to_string(question_number, 'item'), format_list_of_arrays(arrays)),
        (append_question_number_to_string(question_number, 'correct_algorithms'), append_question_number_to_string(question_number, 'correct_algorithm'), format_list_of_integers(correct_algorithms)),
    ]

# Set the folder where XML and images will be saved
folder_path = r"/Users/antemaric/Desktop/Bachelorarbeit/Thesis-Bachelor/Exercise_5"

clear_variable_declarations(folder_path)

num_calls = 40

# Generate exercises for all algorithms (each variant will use a random algorithm)
question_number = 1
result = guess_algorithm_exercise(question_number, num_calls)
exercise_constants = []
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