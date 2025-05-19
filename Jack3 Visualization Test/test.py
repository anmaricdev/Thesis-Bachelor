import random
import json
from datetime import datetime
from formatter_for_copy_paste_export_to_jack3 import *
from formatter_to_xml import format_to_xml, clear_variable_declarations
from append_question_number_to_string import append_question_number_to_string
import base64
import glob
import os
import sys
import shutil

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import from the correct module path
from Bin_Packing_Algorithms import (
    get_random_capacities_and_items,
    visualize_bin_packing,
    bin_packing_best_fit_var_capa,
    bin_packing_first_fit_var_capa,
    bin_packing_next_fit_var_capa,
    bin_packing_worst_fit_var_capa
)
import matplotlib.pyplot as plt

def generate_solution_regex(answer: str) -> str:
    solution = answer
    solution = solution.replace(" ", "").replace(",", r"\s*,\s*").replace("[", r"\[*\s*").replace("]", r"\s*\]*")
    solution = fr"\[*\s*{solution}\s*\]*"
    return f"{solution}"

def get_algorithm_folder_name(algorithm):
    mapping = {
        "BEST": "BEST FIT",
        "FIRST": "FIRST FIT",
        "NEXT": "NEXT FIT",
        "WORST": "WORST FIT"
    }
    return mapping.get(algorithm, algorithm.upper())

def get_algorithm_file_prefix(algorithm):
    mapping = {
        "BEST": "BEST_FIT",
        "FIRST": "FIRST_FIT",
        "NEXT": "NEXT_FIT",
        "WORST": "WORST_FIT"
    }
    return mapping.get(algorithm, algorithm.upper())

def get_bin_packing_sequence(question_number, num_calls, approach: str):
    print(f"Generating bin packing sequence for approach: {approach}")  # Debug print
    bin_capacities_list = []
    items_list = []
    tree_image_file_names = []
    packing_results = []
    images_information = []

    # All images go directly into the base folder_path (no subfolders)
    imgs_folder_path = folder_path
    os.makedirs(imgs_folder_path, exist_ok=True)

    for i in range(num_calls):
        # Generate random parameters for bin packing
        min_bin_count = 3
        max_bin_count = 5
        min_bin_capacity = 8
        max_bin_capacity = 15  # Capped at 15
        min_item_count = 8
        max_item_count = 12
        min_item_size = 1
        max_item_size = 8
        variable_size = random.choice([True, False])

        # Get random capacities and items
        bin_capacities, items = get_random_capacities_and_items(
            min_bin_count, max_bin_count,
            min_bin_capacity, max_bin_capacity,
            min_item_count, max_item_count,
            min_item_size, max_item_size,
            variable_size
        )

        # Create figure with minimal size
        fig = plt.figure(figsize=(12, 4))  # Reduced figure size
        
        # Apply the correct algorithm based on approach (always use the correct function from BinPackingAlgorithms.py)
        if approach == "BEST":
            result = bin_packing_best_fit_var_capa(bin_capacities.copy(), items.copy())
        elif approach == "FIRST":
            result = bin_packing_first_fit_var_capa(bin_capacities.copy(), items.copy())
        elif approach == "NEXT":
            result = bin_packing_next_fit_var_capa(bin_capacities.copy(), items.copy())
        elif approach == "WORST":
            result = bin_packing_worst_fit_var_capa(bin_capacities.copy(), items.copy())
        else:
            raise ValueError(f"Unknown approach: {approach}")
            
        # Use the result to visualize bin packing
        fig = visualize_bin_packing(bin_capacities, items, visualize_in_2d=False, algorithms=[approach])
        
        # Generate a unique filename using only the timestamp (to microseconds)
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        tree_image_file_name = f"{timestamp_str}.png"
        timestamp = datetime.now().isoformat()
        
        # Save the figure to the base folder with tight bounding box
        save_path = os.path.join(imgs_folder_path, tree_image_file_name)
        print(f"Saving image to: {save_path}")  # Debug print
        
        # Adjust figure to remove excess white space
        plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)  # Minimize margins
        fig.tight_layout(pad=0)  # No padding
        
        # Save with minimal padding
        fig.savefig(save_path, 
                   format='png',
                   bbox_inches='tight',
                   pad_inches=0,
                   dpi=300,
                   transparent=False)
        
        # Read the saved file and convert to base64
        with open(save_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        # Close the figure after saving
        plt.close(fig)
        
        bin_capacities_list.append(bin_capacities)
        items_list.append(items)
        tree_image_file_names.append(tree_image_file_name)
        packing_results.append(f"Approach: {approach}, Bins: {len(bin_capacities)}, Items: {len(items)}")
        images_information.append((tree_image_file_name, image_data, timestamp))

    def transform_list_to_string(l: list):
        return ','.join(map(str, l))
    
    bin_capacities_strings = list(map(lambda x: transform_list_to_string(x), bin_capacities_list))
    items_strings = list(map(lambda x: transform_list_to_string(x), items_list))
    packing_results_regex = list(map(generate_solution_regex, packing_results))
    
    return [
        (append_question_number_to_string(question_number, 'bin_capacities'), append_question_number_to_string(question_number, 'bin_capacity'), format_list_of_arrays(bin_capacities_list)),
        (append_question_number_to_string(question_number, 'items'), append_question_number_to_string(question_number, 'item'), format_list_of_arrays(items_list)),
        (append_question_number_to_string(question_number, 'packing_results'), append_question_number_to_string(question_number, 'packing_result'), format_list_of_strings(packing_results)),
        (append_question_number_to_string(question_number, 'packing_results_regex'), append_question_number_to_string(question_number, 'packing_result_regex'), format_list_of_strings(packing_results_regex))
    ], images_information

def generate_task_for_best_fit(question_number, num_calls):
    return get_bin_packing_sequence(question_number, num_calls, "BEST")

def generate_task_for_first_fit(question_number, num_calls):
    return get_bin_packing_sequence(question_number, num_calls, "FIRST")

def generate_task_for_next_fit(question_number, num_calls):
    return get_bin_packing_sequence(question_number, num_calls, "NEXT")

def generate_task_for_worst_fit(question_number, num_calls):
    return get_bin_packing_sequence(question_number, num_calls, "WORST")

# Create the output directories if they don't exist
folder_path = os.path.join(parent_dir, "Generated Pictures")

def generate_exercises(algorithms=None, num_calls=2):
    """
    Generate exercises for specified algorithms.
    
    Args:
        algorithms: List of algorithms to use (e.g., ["BEST", "FIRST"]). If None, uses all algorithms.
        num_calls: Number of exercises to generate per algorithm
    """
    # Only create the base folder_path
    os.makedirs(folder_path, exist_ok=True)

    clear_variable_declarations(folder_path)

    # Dictionary mapping algorithms to their question numbers
    algorithm_questions = {
        "BEST": 2,
        "FIRST": 3,
        "NEXT": 4,
        "WORST": 5
    }

    # If no algorithms specified, use all
    if not algorithms:
        algorithms = list(algorithm_questions.keys())

    all_images = []
    for algorithm in algorithms:
        print(f"Processing algorithm: {algorithm}")  # Debug print
        question_number = algorithm_questions[algorithm]
        result, images = generate_task_for_algorithm(algorithm, question_number, num_calls)
        format_to_xml(
            folder_path,  # Save XML in the base folder
            result, 
            question_number, 
            num_calls, 
            [("question_{}_image_id".format(question_number), 
              f"[var=image_ids_start] + {str(num_calls*list(algorithm_questions.keys()).index(algorithm))} + [var=index_question_{question_number}]")]
        )
        all_images.extend(images)

def generate_task_for_algorithm(algorithm, question_number, num_calls):
    """Generate tasks for a specific algorithm."""
    if algorithm == "BEST":
        return generate_task_for_best_fit(question_number, num_calls)
    elif algorithm == "FIRST":
        return generate_task_for_first_fit(question_number, num_calls)
    elif algorithm == "NEXT":
        return generate_task_for_next_fit(question_number, num_calls)
    elif algorithm == "WORST":
        return generate_task_for_worst_fit(question_number, num_calls)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")

# Example usage:
if __name__ == "__main__":
    # Generate exercises for specific algorithms
    # Examples:
    # generate_exercises(["BEST"])  # Only Best Fit
    generate_exercises(["NEXT"])  # Current example: only Worst Fit