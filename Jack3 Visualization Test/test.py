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

def get_bin_packing_sequence(question_number, num_calls, approach: str):
    ARRAY_LENGTH = 7
    bin_capacities_list = []
    items_list = []
    tree_image_file_names = []
    packing_results = []
    images_information = []
    
    for i in range(num_calls):
        # Generate random parameters for bin packing
        min_bin_count = 3
        max_bin_count = 5
        min_bin_capacity = 8
        max_bin_capacity = 15  # Reduced from 20 to 15
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

        # Create figure and generate visualization
        fig = plt.figure(figsize=(15, 15))
        fig = visualize_bin_packing(bin_capacities, items, visualize_in_2d=False)
        
        # Generate a sequential ID for the image
        image_id = f"{question_number:02d}_{i+1:03d}"  # Format: question_number_sequence (e.g., 02_001)
        tree_image_file_name = f"bin_packing_{image_id}.png"
        timestamp = datetime.now().isoformat()
        
        # Save the figure to the imgs subfolder
        save_path = os.path.join(imgs_folder_path, tree_image_file_name)
        print(f"Saving image to: {save_path}")  # Debug print
        fig.savefig(save_path, format='png', bbox_inches='tight', dpi=300)
        
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
# Create a timestamped folder for this run
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
run_folder = os.path.join(folder_path, f"run_{timestamp}")
imgs_folder_path = os.path.join(run_folder, "imgs")
os.makedirs(folder_path, exist_ok=True)
os.makedirs(run_folder, exist_ok=True)
os.makedirs(imgs_folder_path, exist_ok=True)

clear_variable_declarations(folder_path)

# Clean up existing images in the imgs folder BEFORE generating new ones
for image_file in glob.glob(os.path.join(imgs_folder_path, "bin_packing_*.png")):
    os.remove(image_file)

num_calls = 2 # 2 exercises per algorithm (8 total)
all_images = []

question_number = 2
result, images = generate_task_for_best_fit(question_number, num_calls)
format_to_xml(run_folder, result, question_number, num_calls, [("image_ids_start", "Put image start id here"), ("question_2_image_id", f"[var=image_ids_start] + {str(num_calls*0)} + [var=index_question_2]")])
all_images.extend(images)

question_number = 3
result, images = generate_task_for_first_fit(question_number, num_calls)
format_to_xml(run_folder, result, question_number, num_calls, [("question_3_image_id", f"[var=image_ids_start] + {str(num_calls*1)} + [var=index_question_3]")])
all_images.extend(images)

question_number = 4
result, images = generate_task_for_next_fit(question_number, num_calls)
format_to_xml(run_folder, result, question_number, num_calls, [("question_4_image_id", f"[var=image_ids_start] + {str(num_calls*2)} + [var=index_question_4]")])
all_images.extend(images)

question_number = 5
result, images = generate_task_for_worst_fit(question_number, num_calls)
format_to_xml(run_folder, result, question_number, num_calls, [("question_5_image_id", f"[var=image_ids_start] + {str(num_calls*3)} + [var=index_question_5]")])
all_images.extend(images)

# No need to save images again as they were already saved during generation
