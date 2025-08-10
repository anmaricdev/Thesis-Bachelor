# Exercise 7: Item List Optimization
# This script creates exercises where the user has to optimize the order of items
# to minimize leftover items for a given bin packing algorithm.

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
import itertools

def generate_solution_regex(answer: str) -> str:
    solution = answer
    solution = solution.replace(" ", "")
    # Accept the leftover amount as a single number
    # Students provide the minimum leftover capacity that can be achieved
    solution = fr"^\s*{solution}\s*$"
    return solution

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

def calculate_leftover(algorithm, bin_capacities, items):
    """Calculate the total leftover capacity for a given algorithm and item order."""
    is_possible, bins, bins_packed_after_failure = run_algorithm(algorithm, bin_capacities, items)
    
    # Get items that were successfully packed (each item is already an integer size)
    packed_items = [item for bin_items in bins for item in bin_items]
    
    # Calculate leftover capacity (total size of items that couldn't be packed)
    total_packed_size = sum(packed_items)  # packed_items are integers (sizes)
    total_items_size = sum(items)  # items is list of integers (sizes)
    leftover_capacity = total_items_size - total_packed_size
    
    return leftover_capacity, bins

def find_optimal_ordering(algorithm, bin_capacities, items):
    """Find the optimal ordering of items that minimizes leftover."""
    min_leftover = float('inf')
    optimal_ordering = items.copy()
    
    # Try all possible permutations of items
    for perm in itertools.permutations(items):
        leftover, _ = calculate_leftover(algorithm, bin_capacities, list(perm))
        if leftover < min_leftover:
            min_leftover = leftover
            optimal_ordering = list(perm)
    
    return optimal_ordering, min_leftover

def find_optimal_ordering_fast(algorithm, bin_capacities, items):
    """Find the true optimal ordering by checking all permutations."""
    # With reduced complexity (max 5 items), we can always check all permutations
    # This ensures we get the actual optimal solution
    
    return find_optimal_ordering(algorithm, bin_capacities, items)

def item_list_optimization_exercise(question_number, num_calls, algorithm):
    # Parameters for random generation - REDUCED COMPLEXITY
    min_bin_count, max_bin_count = 2, 3  # Reduced from 2-4 to 2-3
    min_bin_capacity, max_bin_capacity = 4, 8  # Reduced from 6-12 to 4-8
    min_item_count, max_item_count = 3, 5  # Reduced from 5-7 to 3-5
    min_item_size, max_item_size = 2, 6  # Reduced from 2-8 to 2-6

    arrays = []
    bin_capacities_list = []
    optimal_orderings = []
    optimal_leftover_regexes = []
    original_leftover_capacities = []
    optimal_leftover_capacities = []
    image_filenames = []

    for i in range(num_calls):
        max_attempts = 50  # Reduced since we're using fast method now
        successful_generation = False
        
        for attempt in range(max_attempts):
            # Generate random bins and items
            bin_count = random.randint(min_bin_count, max_bin_count)
            bin_capacities = [random.randint(min_bin_capacity, max_bin_capacity) for _ in range(bin_count)]
            item_count = random.randint(min_item_count, max_item_count)
            items = [random.randint(min_item_size, max_item_size) for _ in range(item_count)]
            
            # CRITICAL: Ensure guaranteed leftovers for meaningful optimization
            total_capacity = sum(bin_capacities)
            total_items = sum(items)
            
            # Method 1: Ensure items exceed capacity (guaranteed leftover)
            if total_items <= total_capacity * 0.9:  # Too easy - regenerate
                continue
                
            # Method 2: Ensure at least one item is too large for any bin
            max_bin = max(bin_capacities)
            if max(items) <= max_bin:  # All items fit individually
                # Add a large item that can't fit anywhere
                oversized_item = max_bin + random.randint(1, 3)
                items.append(oversized_item)
                item_count += 1  # Update item count
            
            # Method 3: Ensure we have enough items for meaningful permutations
            if item_count < 4:  # Need at least 4 items for good optimization potential
                continue
            
            # Verify we actually have leftovers
            original_leftover, _ = calculate_leftover(algorithm, bin_capacities, items)
            if original_leftover == 0:  # No leftover - regenerate
                continue
                
            # Calculate leftover for original (unsorted) order
            original_leftover, original_bins = calculate_leftover(algorithm, bin_capacities, items)
            
            # Find optimal ordering using fast method
            optimal_ordering, optimal_leftover = find_optimal_ordering_fast(algorithm, bin_capacities, items)
            
            # Accept this solution - multiple optimal solutions are fine and realistic
            print(f"    Found optimal solution with {optimal_leftover} leftover capacity")
            
            # Only use this variant if there's actually an improvement possible
            if optimal_leftover < original_leftover:
                # Ensure original ordering is NOT optimal by shuffling
                shuffled_items = copy.deepcopy(items)
                shuffled_bin_capacities = copy.deepcopy(bin_capacities)
                
                # Force a suboptimal original ordering by shuffling items
                random.shuffle(shuffled_items)
                random.shuffle(shuffled_bin_capacities)
                
                # Recalculate with shuffled values
                shuffled_original_leftover, _ = calculate_leftover(algorithm, shuffled_bin_capacities, shuffled_items)
                shuffled_optimal_ordering, shuffled_optimal_leftover = find_optimal_ordering_fast(algorithm, shuffled_bin_capacities, shuffled_items)
                
                # Accept shuffled solution - multiple optimal solutions are fine
                print(f"    Found shuffled optimal solution with {shuffled_optimal_leftover} leftover capacity")
                
                # Ensure we still have improvement after shuffling
                if shuffled_optimal_leftover < shuffled_original_leftover:
                    # Ensure original and optimal are actually different orderings
                    if shuffled_optimal_ordering != shuffled_items:
                        # Generate regex for the optimal leftover amount
                        optimal_leftover_str = str(shuffled_optimal_leftover)
                        optimal_leftover_regex = generate_solution_regex(optimal_leftover_str)
                        
                        successful_generation = True
                        break  # Exit the attempt loop
                    else:
                        # Original and optimal are the same, try again
                        continue
                else:
                    # Shuffling didn't create improvement, try again
                    continue
        
        # Only proceed if we successfully generated a problem with guaranteed leftovers
        if not successful_generation:
            print(f"  FAILED: Could not generate valid problem for {algorithm} after {max_attempts} attempts")
            continue
            
        # Save the EXERCISE image (show original unsorted state)
        fig_exercise = visualize_bin_packing(
            shuffled_bin_capacities,
            shuffled_items,
            visualize_in_2d=False,
            algorithms=[algorithm],
            visualization_options={
                "hide_leftover": False,  # Show leftover to demonstrate the problem
                "hide_solution": True,   # Hide algorithm name
                "show_items_list": True,
                "hide_bin_filling": False,
                "hide_used_info": False,
                "hide_failure": True     # Hide the cross/failure indicator
            }
        )
        exercise_image_filename = f"Exercise_{question_number}_{algorithm}_variant_{i+1}.png"
        exercise_image_path = os.path.join(folder_path, exercise_image_filename)
        fig_exercise.savefig(exercise_image_path, format='png', bbox_inches='tight', pad_inches=0, dpi=150)
        plt.close(fig_exercise)

        arrays.append(shuffled_items)
        bin_capacities_list.append(shuffled_bin_capacities)
        optimal_orderings.append(shuffled_optimal_ordering)
        optimal_leftover_regexes.append(optimal_leftover_regex)
        original_leftover_capacities.append(shuffled_original_leftover)
        optimal_leftover_capacities.append(shuffled_optimal_leftover)
        image_filenames.append(exercise_image_filename)

        print(f"Variant {i+1}: {algorithm} - Original leftover capacity: {shuffled_original_leftover}, Optimal leftover capacity: {shuffled_optimal_leftover}")
        print(f"  Original: {shuffled_items}")
        print(f"  Optimal: {shuffled_optimal_ordering}")

    return [
        (append_question_number_to_string(question_number, 'bin_capacities'), append_question_number_to_string(question_number, 'bin_capacity'), format_list_of_arrays(bin_capacities_list)),
        (append_question_number_to_string(question_number, 'items'), append_question_number_to_string(question_number, 'item'), format_list_of_arrays(arrays)),
        (append_question_number_to_string(question_number, 'optimal_orderings'), append_question_number_to_string(question_number, 'optimal_ordering'), format_list_of_arrays(optimal_orderings)),
        (append_question_number_to_string(question_number, 'optimal_leftover_regexes'), append_question_number_to_string(question_number, 'optimal_leftover_regex'), format_list_of_strings(optimal_leftover_regexes)),
        (append_question_number_to_string(question_number, 'original_leftover_capacities'), append_question_number_to_string(question_number, 'original_leftover_capacity'), format_list_of_integers(original_leftover_capacities)),
        (append_question_number_to_string(question_number, 'optimal_leftover_capacities'), append_question_number_to_string(question_number, 'optimal_leftover_capacity'), format_list_of_integers(optimal_leftover_capacities)),
    ]

# Set the folder where XML and images will be saved
folder_path = r"/Users/antemaric/Desktop/Bachelorarbeit/Thesis-Bachelor/Exercise_7"

clear_variable_declarations(folder_path)

num_calls = 10

algorithms = ["BEST", "FIRST", "NEXT", "WORST"]
for idx, algorithm in enumerate(algorithms, start=1):
    question_number = idx
    result = item_list_optimization_exercise(question_number, num_calls, algorithm)
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