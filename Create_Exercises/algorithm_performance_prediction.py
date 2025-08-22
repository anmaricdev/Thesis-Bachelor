# Exercise 6: Algorithm Performance Prediction
# This script creates exercises where the user has to predict which algorithm will use the fewest bins for a given problem.

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

def run_algorithm(algorithm, items, capacities):
    """Run a specific algorithm and return number of bins used"""
    if algorithm == "BEST":
        is_possible, used_bins, _ = bin_packing_best_fit_var_capa(capacities.copy(), items.copy())
    elif algorithm == "FIRST":
        is_possible, used_bins, _ = bin_packing_first_fit_var_capa(capacities.copy(), items.copy())
    elif algorithm == "NEXT":
        is_possible, used_bins, _ = bin_packing_next_fit_var_capa(capacities.copy(), items.copy())
    elif algorithm == "WORST":
        is_possible, used_bins, _ = bin_packing_worst_fit_var_capa(capacities.copy(), items.copy())
    
    # Count non-empty bins
    bins_used = len([bin_items for bin_items in used_bins if bin_items])
    return bins_used, used_bins

def validate_unique_solution(items, bin_capacities):
    """Validate that exactly one algorithm is optimal"""
    algorithms = ["BEST", "FIRST", "NEXT", "WORST"]
    
    results = {}
    for algo in algorithms:
        bins_used, _ = run_algorithm(algo, items, bin_capacities)
        results[algo] = bins_used
    
    # Find the best result
    min_bins = min(results.values())
    best_algorithms = [algo for algo, bins in results.items() if bins == min_bins]
    
    return len(best_algorithms) == 1, best_algorithms[0], results

def generate_best_fit_optimal_problem():
    """Generate problems where Best Fit is clearly optimal"""
    # Best Fit works well when items can be tightly packed with varying capacities
    problems = [
        {"items": [6, 2, 4, 3, 2, 3], "bin_capacities": [6, 8, 10]},
        {"items": [5, 3, 4, 2, 3, 3], "bin_capacities": [7, 9, 8]},
        {"items": [7, 1, 6, 2, 5, 3], "bin_capacities": [8, 6, 10]},
        {"items": [4, 4, 5, 3, 3, 2], "bin_capacities": [5, 7, 9]},
        {"items": [6, 2, 3, 3, 2, 3], "bin_capacities": [6, 8, 7]}
    ]
    return random.choice(problems)

def generate_first_fit_optimal_problem():
    """Generate problems where First Fit performs well"""
    # First Fit works well with mixed item sizes and specific patterns
    problems = [
        {"items": [3, 3, 3, 3, 3, 3], "bin_capacities": [4, 6, 8, 10]},
        {"items": [2, 4, 2, 4, 2, 4], "bin_capacities": [3, 5, 7, 9]},
        {"items": [1, 5, 1, 5, 1, 5], "bin_capacities": [2, 4, 6, 8]},
        {"items": [4, 2, 4, 2, 4, 2], "bin_capacities": [5, 7, 9, 11]},
        {"items": [1, 6, 1, 6, 1, 6], "bin_capacities": [2, 4, 6, 8]}
    ]
    return random.choice(problems)

def generate_next_fit_optimal_problem():
    """Generate problems where Next Fit is optimal"""
    # Next Fit works well with sequential patterns and specific capacities
    problems = [
        {"items": [4, 2, 4, 2, 4, 2], "bin_capacities": [8, 8, 8, 8]},
        {"items": [3, 3, 3, 3, 3, 3], "bin_capacities": [8, 8, 8, 8]},
        {"items": [5, 1, 5, 1, 5, 1], "bin_capacities": [8, 8, 8, 8]},
        {"items": [2, 4, 2, 4, 2, 4], "bin_capacities": [8, 8, 8, 8]},
        {"items": [6, 0, 6, 0, 6, 0], "bin_capacities": [8, 8, 8, 8]}
    ]
    return random.choice(problems)

def generate_worst_fit_optimal_problem():
    """Generate problems where Worst Fit performs well"""
    # Worst Fit works well with many small items and specific capacities
    problems = [
        {"items": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], "bin_capacities": [2, 4, 6, 8]},
        {"items": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], "bin_capacities": [3, 5, 7, 9, 11]},
        {"items": [2, 2, 2, 2, 2, 2, 2, 2], "bin_capacities": [4, 6, 8, 10]},
        {"items": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], "bin_capacities": [2, 4, 6, 8, 10]},
        {"items": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], "bin_capacities": [3, 5, 7, 9, 11, 13]}
    ]
    return random.choice(problems)

def generate_validated_problem(target_algorithm):
    """Generate a problem that validates for the target algorithm"""
    max_attempts = 50
    
    for attempt in range(max_attempts):
        if target_algorithm == "BEST":
            problem = generate_best_fit_optimal_problem()
        elif target_algorithm == "FIRST":
            problem = generate_first_fit_optimal_problem()
        elif target_algorithm == "NEXT":
            problem = generate_next_fit_optimal_problem()
        elif target_algorithm == "WORST":
            problem = generate_worst_fit_optimal_problem()
        
        is_unique, best_algo, results = validate_unique_solution(problem["items"], problem["bin_capacities"])
        
        if is_unique and best_algo == target_algorithm:
            return problem, results
    
    # If predefined problems don't work, try generating random problems
    print(f"  Trying random problem generation for {target_algorithm}...")
    for attempt in range(50):  # Increased attempts
        # Generate random problem with more variety
        bin_count = random.randint(2, 4)
        bin_capacities = [random.randint(4, 12) for _ in range(bin_count)]  # Reduced from 5-20 to 4-12
        item_count = random.randint(3, 8)  # Reduced from 3-10 to 3-8
        items = [random.randint(1, 8) for _ in range(item_count)]  # Reduced from 1-12 to 1-8
        
        # Ensure items can actually fit in bins
        total_item_size = sum(items)
        total_bin_capacity = sum(bin_capacities)
        if total_item_size > total_bin_capacity * 0.8:  # Don't make it too tight
            continue
        
        is_unique, best_algo, results = validate_unique_solution(items, bin_capacities)
        
        if is_unique and best_algo == target_algorithm:
            return {"items": items, "bin_capacities": bin_capacities}, results
    
    # Last resort: return a simple problem that at least works
    print(f"  Using fallback problem for {target_algorithm}...")
    if target_algorithm == "BEST":
        return {"items": [6, 2, 4, 3], "bin_capacities": [6, 8, 10]}, {"BEST": 2, "FIRST": 3, "NEXT": 3, "WORST": 3}
    elif target_algorithm == "FIRST":
        return {"items": [3, 3, 3, 3], "bin_capacities": [4, 6, 8]}, {"BEST": 2, "FIRST": 2, "NEXT": 3, "WORST": 3}
    elif target_algorithm == "NEXT":
        return {"items": [4, 2, 4, 2], "bin_capacities": [8, 8, 8]}, {"BEST": 2, "FIRST": 2, "NEXT": 2, "WORST": 3}
    else:  # WORST
        return {"items": [1, 1, 1, 1, 1, 1], "bin_capacities": [2, 4, 6]}, {"BEST": 2, "FIRST": 2, "NEXT": 2, "WORST": 2}

def algorithm_performance_prediction_exercise(question_number, num_calls):
    """Generate algorithm performance prediction exercises"""
    
    arrays = []
    bin_capacities_list = []
    correct_algorithms = []
    image_filenames = []
    all_results = []  # Store results for all algorithms for each variant

    # Algorithm mapping for student input (0-based indexing)
    algorithm_mapping = {
        "BEST": 0,
        "FIRST": 1, 
        "NEXT": 2,
        "WORST": 3
    }

    # Ensure balanced distribution - each algorithm gets num_calls // 4 exercises
    algorithms_per_variant = num_calls // 4
    remaining = num_calls % 4
    
    # Create algorithm list with balanced distribution
    algorithm_list = []
    for algo in ["BEST", "FIRST", "NEXT", "WORST"]:
        count = algorithms_per_variant + (1 if remaining > 0 else 0)
        algorithm_list.extend([algo] * count)
        remaining -= 1
    
    # Shuffle the algorithm list to randomize order
    random.shuffle(algorithm_list)
    
    successful_variant_count = 0
    max_total_attempts = num_calls * 10  # Allow up to 10x more attempts to find solutions
    total_attempts = 0
    
    # Keep trying until we get exactly num_calls successful variants
    while successful_variant_count < num_calls and total_attempts < max_total_attempts:
        total_attempts += 1
        
        # Cycle through the algorithm list
        target_algorithm = algorithm_list[successful_variant_count % len(algorithm_list)]
        
        print(f"Attempt {total_attempts}: Generating variant {successful_variant_count + 1} for {target_algorithm} algorithm...")
        
        # Generate problem for this algorithm using predefined problems
        problem, results = generate_validated_problem(target_algorithm)
        
        # Validate the solution is unique
        is_unique, best_algo, actual_results = validate_unique_solution(problem["items"], problem["bin_capacities"])
        
        if is_unique and best_algo == target_algorithm:
            # Try multiple shuffles to find one that maintains the target algorithm as optimal
            max_shuffle_attempts = 20
            successful_shuffle = False
            
            for shuffle_attempt in range(max_shuffle_attempts):
                # Randomize order for variety
                shuffled_items = copy.deepcopy(problem["items"])
                shuffled_bin_capacities = copy.deepcopy(problem["bin_capacities"])
                random.shuffle(shuffled_items)
                random.shuffle(shuffled_bin_capacities)
                
                # CRITICAL FIX: Re-validate that the target algorithm is still optimal after shuffling
                is_unique_after_shuffle, best_algo_after_shuffle, actual_results_after_shuffle = validate_unique_solution(shuffled_items, shuffled_bin_capacities)
                
                if is_unique_after_shuffle and best_algo_after_shuffle == target_algorithm:
                    successful_shuffle = True
                    break
            
            if successful_shuffle:
                successful_variant_count += 1
                
                # Create EMPTY visualization for the question (no algorithm result)
                fig_empty = visualize_bin_packing(
                    shuffled_bin_capacities,
                    shuffled_items,
                    visualize_in_2d=False,
                    algorithms=[],  # No algorithms - just show the problem
                    visualization_options={
                        "hide_leftover": True,   # Hide leftover since no algorithm was run
                        "hide_solution": True,   # Hide solution info
                        "show_items_list": False, # Show items list
                        "hide_bin_filling": True, # Hide bin filling since no algorithm was run
                        "hide_used_info": True,   # Hide used info
                        "hide_algorithm_name": True  # Hide algorithm name
                    }
                )
                
                # Create FILLED visualization for the solution (with algorithm result)
                fig_filled = visualize_bin_packing(
                    shuffled_bin_capacities,
                    shuffled_items,
                    visualize_in_2d=False,
                    algorithms=[target_algorithm],  # Show the optimal algorithm
                    visualization_options={
                        "hide_leftover": False,  # Show leftover items
                        "hide_solution": False,  # Show algorithm name and success status
                        "show_items_list": False, # Show items list
                        "hide_bin_filling": False, # Show how bins are filled
                        "hide_used_info": False,   # Show used info
                        "hide_algorithm_name": False  # Show algorithm name
                    }
                )
                
                # Generate image filenames
                question_image_filename = f"Exercise_variant_{successful_variant_count}_{question_number}_{target_algorithm}.png"
                solution_image_filename = f"Solution_variant_{successful_variant_count}_{question_number}_{target_algorithm}.png"
                
                question_image_path = os.path.join(folder_path, question_image_filename)
                solution_image_path = os.path.join(folder_path, solution_image_filename)
                
                # Save both images
                fig_empty.savefig(question_image_path, format='png', bbox_inches='tight', pad_inches=0, dpi=150)
                fig_filled.savefig(solution_image_path, format='png', bbox_inches='tight', pad_inches=0, dpi=150)
                plt.close(fig_empty)
                plt.close(fig_filled)
                
                # Create solution (algorithm index: 0=Best, 1=First, 2=Next, 3=Worst)
                solution = algorithm_mapping[target_algorithm]
                
                # Store exercise data
                arrays.append(shuffled_items)
                bin_capacities_list.append(shuffled_bin_capacities)
                correct_algorithms.append(solution)
                image_filenames.append(question_image_filename)  # Use question image for the exercise
                
                # Store results for all algorithms (for detailed feedback) - use shuffled results
                all_results.append(actual_results_after_shuffle)
                
                # Helpful debugging information
                print(f"  SUCCESS: Variant {successful_variant_count} - {target_algorithm} algorithm (index {solution})")
                print(f"    Items: {shuffled_items}")
                print(f"    Bin capacities: {shuffled_bin_capacities}")
                print(f"    Results: {actual_results_after_shuffle}")
            else:
                print(f"  FAILED: Could not find a shuffle that maintains {target_algorithm} as optimal")
                print(f"    Tried {max_shuffle_attempts} shuffles")
                print(f"    Original results: {actual_results}")
        else:
            print(f"  FAILED: Could not validate unique solution for {target_algorithm}")
            print(f"    Expected: {target_algorithm}, Got: {best_algo}")
            print(f"    Results: {actual_results}")

    # Debug: Print the final correct_algorithms list
    print(f"\nFINAL RESULTS:")
    print(f"Generated {successful_variant_count} successful variants out of {num_calls} requested")
    print(f"Total attempts: {total_attempts}")
    print(f"Algorithm distribution:")
    algo_counts = {}
    for alg_idx in correct_algorithms:
        alg_name = {0: "BEST", 1: "FIRST", 2: "NEXT", 3: "WORST"}[alg_idx]
        algo_counts[alg_name] = algo_counts.get(alg_name, 0) + 1
    
    for algo, count in algo_counts.items():
        print(f"  {algo}: {count} exercises")
    
    if successful_variant_count < num_calls:
        print(f"WARNING: Only generated {successful_variant_count} variants instead of {num_calls}")
    
    # Format results for JACK3 variables
    best_fit_results = [results["BEST"] for results in all_results]
    first_fit_results = [results["FIRST"] for results in all_results]
    next_fit_results = [results["NEXT"] for results in all_results]
    worst_fit_results = [results["WORST"] for results in all_results]
    
    return [
        (append_question_number_to_string(question_number, 'bin_capacities'), append_question_number_to_string(question_number, 'bin_capacity'), format_list_of_arrays(bin_capacities_list)),
        (append_question_number_to_string(question_number, 'items'), append_question_number_to_string(question_number, 'item'), format_list_of_arrays(arrays)),
        (append_question_number_to_string(question_number, 'correct_algorithms'), append_question_number_to_string(question_number, 'correct_algorithm'), format_list_of_integers(correct_algorithms)),
        (append_question_number_to_string(question_number, 'best_fit_results'), append_question_number_to_string(question_number, 'best_fit_result'), format_list_of_integers(best_fit_results)),
        (append_question_number_to_string(question_number, 'first_fit_results'), append_question_number_to_string(question_number, 'first_fit_result'), format_list_of_integers(first_fit_results)),
        (append_question_number_to_string(question_number, 'next_fit_results'), append_question_number_to_string(question_number, 'next_fit_result'), format_list_of_integers(next_fit_results)),
        (append_question_number_to_string(question_number, 'worst_fit_results'), append_question_number_to_string(question_number, 'worst_fit_result'), format_list_of_integers(worst_fit_results)),
    ]

# Set the folder where XML and images will be saved
folder_path = r"/Users/antemaric/Desktop/Bachelorarbeit/Thesis-Bachelor/Exercise_6"

clear_variable_declarations(folder_path)

num_calls = 20

# Generate exercises for all algorithms (each variant will use a random algorithm)
question_number = 1
result = algorithm_performance_prediction_exercise(question_number, num_calls)
exercise_constants = []
solution_constants = []
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