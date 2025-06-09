import random
import matplotlib.pyplot as plt
import base64
import glob
import os
import sys
from datetime import datetime

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import formatters - using the correct directory name with spaces
sys.path.append(os.path.join(current_dir, "Test XML"))
from formatter_for_copy_paste_export_to_jack3 import *
from formatter_to_xml import format_to_xml, clear_variable_declarations
from append_question_number_to_string import append_question_number_to_string

# Import bin packing modules
from Visualization import visualize_bin_packing
from HelperFuncRand import get_random_capacities_and_items
from BinPackingAlgorithms import (
    bin_packing_best_fit_var_capa,
    bin_packing_first_fit_var_capa,
    bin_packing_next_fit_var_capa,
    bin_packing_worst_fit_var_capa
)

# Constants for exercise generation
VARIANTS_PER_EXERCISE = 2  # Number of variants for each exercise type
EXERCISE_TYPES = {
    "BEST": 2,    # Exercise 2: Best Fit
    "FIRST": 3,   # Exercise 3: First Fit
    "NEXT": 4,    # Exercise 4: Next Fit
    "WORST": 5    # Exercise 5: Worst Fit
}

def create_initial_xml(folder_path):
    """Create an initial XML file if it doesn't exist."""
    xml_path = os.path.join(folder_path, "bin_packing.xml")
    if not os.path.exists(xml_path):
        initial_xml = """<?xml version="1.0" encoding="UTF-8"?>
<exercise>
    <variableDeclarations id="1">
    </variableDeclarations>
</exercise>"""
        with open(xml_path, 'w', encoding='utf-8') as f:
            f.write(initial_xml)
    return xml_path

def generate_solution_regex(answer: str) -> str:
    """Generate a regex pattern for the solution."""
    solution = answer
    solution = solution.replace(" ", "").replace(",", r"\s*,\s*").replace("[", r"\[*\s*").replace("]", r"\s*\]*")
    solution = fr"\[*\s*{solution}\s*\]*"
    return f"{solution}"

def get_bin_packing_sequence(exercise_number, variant_number, approach: str):
    """Generate a sequence of bin packing tasks for a specific exercise variant."""
    print(f"Generating variant {variant_number} for exercise {exercise_number} using {approach} approach")
    
    # Generate random parameters for bin packing
    min_bin_count = 2
    max_bin_count = 5
    min_bin_capacity = 8
    max_bin_capacity = 15
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
    fig = plt.figure(figsize=(12, 4))
    
    # Apply the correct algorithm based on approach
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
    
    # Generate filename based on exercise number and variant number
    image_file_name = f"Exercise_{exercise_number}_variant_{variant_number}.png"
    timestamp = datetime.now().isoformat()
    
    # Save the figure to the base folder with tight bounding box
    save_path = os.path.join(folder_path, image_file_name)
    print(f"Saving image to: {save_path}")
    
    # Adjust figure to remove excess white space
    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
    fig.tight_layout(pad=0)
    
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
    
    # Generate the solution string for regex checking
    packing_result = f"Approach: {approach}, Bins: {len(bin_capacities)}, Items: {len(items)}"
    packing_result_regex = generate_solution_regex(packing_result)
    
    return [
        (append_question_number_to_string(exercise_number, 'bin_capacities'), 
         append_question_number_to_string(exercise_number, 'bin_capacity'), 
         format_list_of_arrays([bin_capacities])),
        (append_question_number_to_string(exercise_number, 'items'), 
         append_question_number_to_string(exercise_number, 'item'), 
         format_list_of_arrays([items])),
        (append_question_number_to_string(exercise_number, 'packing_results'), 
         append_question_number_to_string(exercise_number, 'packing_result'), 
         format_list_of_strings([packing_result])),
        (append_question_number_to_string(exercise_number, 'packing_results_regex'), 
         append_question_number_to_string(exercise_number, 'packing_result_regex'), 
         format_list_of_strings([packing_result_regex]))
    ], [(image_file_name, image_data, timestamp)]

def generate_exercises(algorithms=None):
    """
    Generate exercises for specified algorithms.
    Each exercise type will have VARIANTS_PER_EXERCISE variants.
    
    Args:
        algorithms: List of algorithms to use (e.g., ["BEST", "FIRST"]). If None, uses all algorithms.
    """
    # Create the base folder_path
    os.makedirs(folder_path, exist_ok=True)
    
    # Create initial XML file if it doesn't exist
    create_initial_xml(folder_path)

    clear_variable_declarations(folder_path)

    # If no algorithms specified, use all
    if not algorithms:
        algorithms = list(EXERCISE_TYPES.keys())

    all_images = []
    for algorithm in algorithms:
        exercise_number = EXERCISE_TYPES[algorithm]
        print(f"\nGenerating {VARIANTS_PER_EXERCISE} variants for Exercise {exercise_number} ({algorithm} Fit)")
        
        for variant in range(1, VARIANTS_PER_EXERCISE + 1):
            result, images = get_bin_packing_sequence(exercise_number, variant, algorithm)
            format_to_xml(
                folder_path,
                result, 
                exercise_number, 
                1,  # One variant at a time
                [("question_{}_image_id".format(exercise_number), 
                  f"[var=image_ids_start] + {str((variant-1))} + [var=index_question_{exercise_number}]")]
            )
            all_images.extend(images)

# Create the output directories if they don't exist
folder_path = os.path.join(current_dir, "Generated Pictures")

# Example usage:
if __name__ == "__main__":
    # Generate exercises for specific algorithms
    # Examples:
    # generate_exercises(["BEST"])  # Only Best Fit
    generate_exercises(["BEST", "FIRST", "NEXT", "WORST"])  # All algorithms 