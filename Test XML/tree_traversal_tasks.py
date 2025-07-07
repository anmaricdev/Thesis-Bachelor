import random
import json
from datetime import datetime
from formatter_for_copy_paste_export_to_jack3 import *
from formatter_to_xml import format_to_xml, clear_variable_declarations
from append_question_number_to_string import append_question_number_to_string
import create_graph_image
import base64
import glob
import os

import binary_search_tree_sequence as bstree

def generate_solution_regex(answer: str) -> str:
    solution = answer
    solution = solution.replace(" ", "").replace(",", r"\s*,\s*").replace("[", r"\[*\s*").replace("]", r"\s*\]*")
    solution = fr"\[*\s*{solution}\s*\]*"
    return f"{solution}"

def transform_binary_search_tree_to_json(bst: bstree.BST):
    tree = get_subtree_dict(bst.root)
    return json.dumps(tree, indent=4)
    
def get_subtree_dict(node: bstree.Node | None):
    if node is None:
        return "NIL"
    return {
        "value": str(node.data),
        "left": get_subtree_dict(node.left),
        "right": get_subtree_dict(node.right)
    }

def generate_task_for_preorder_traversal_node_sequence(question_number, num_calls):
    return get_traversal_node_sequence(question_number, num_calls, "preorder")

def generate_task_for_inorder_traversal_node_sequence(question_number, num_calls):
    return get_traversal_node_sequence(question_number, num_calls, "inorder")

def generate_task_for_postorder_traversal_node_sequence(question_number, num_calls):
    return get_traversal_node_sequence(question_number, num_calls, "postorder")

def get_traversal_node_sequence(question_number, num_calls, traversal_type: str):
    ARRAY_LENGTH = 7
    arrays = []
    tree_image_file_names = []
    traversal_sequences = []
    images_information = []
    for i in range(num_calls):
        array = random.sample(range(1, 50), ARRAY_LENGTH)
        bst = bstree.BST()
        for element in array:
            bst.root = bstree.insert(bst.root, element)
        tree_image_file_name = f"graph_question_{question_number}_iteration_{i}.png"
        tree_as_json = transform_binary_search_tree_to_json(bst)
        timestamp = datetime.now().isoformat()
        graph_image = create_graph_image.get_graph_image(tree_as_json)
        arrays.append(array)
        traversal_sequences.append(bstree.get_traversal_sequence(bst.root, traversal_type))
        images_information.append((tree_image_file_name, graph_image, timestamp))
    def transform_list_to_string(l: list[int]):
        return ','.join(map(str, l))
    traversal_sequences_strings = list(map(lambda x: transform_list_to_string(x), traversal_sequences))
    traversal_sequences_regex = list(map(generate_solution_regex, traversal_sequences_strings))
    return [
        (append_question_number_to_string(question_number, 'arrays'), append_question_number_to_string(question_number, 'array'), format_list_of_arrays(arrays)),
        (append_question_number_to_string(question_number, 'traversal_sequences'), append_question_number_to_string(question_number, 'traversal_sequence'), format_list_of_strings(traversal_sequences)),
        (append_question_number_to_string(question_number, 'traversal_sequences_regex'), append_question_number_to_string(question_number, 'traversal_sequence_regex'), format_list_of_strings(traversal_sequences_regex))
    ], images_information

folder_path = r"C:\Users\Edwar\Downloads\mytasks\Questions regarding Tree Traversal - Chapter 7.3.2"
imgage_folder_path = r"C:\Users\Edwar\Downloads\mytasks\Questions regarding Tree Traversal - Chapter 7.3.2\imgs"

clear_variable_declarations(folder_path)

num_calls = 25
all_images = []

question_number = 2
result, images = generate_task_for_preorder_traversal_node_sequence(question_number, num_calls)
format_to_xml(folder_path, result, question_number, num_calls, [("image_ids_start", "Put image start id here"), ("question_2_image_id", f"[var=image_ids_start] + {str(num_calls*0)} + [var=index_question_2]")])
all_images.extend(images)

question_number = 3
result, images = generate_task_for_inorder_traversal_node_sequence(question_number, num_calls)
format_to_xml(folder_path, result, question_number, num_calls, [("question_3_image_id", f"[var=image_ids_start] + {str(num_calls*1)} + [var=index_question_3]")])
all_images.extend(images)

question_number = 4
result, images = generate_task_for_postorder_traversal_node_sequence(question_number, num_calls)
format_to_xml(folder_path, result, question_number, num_calls, 
              [("question_4_image_id", f"[var=image_ids_start] + {str(num_calls*2)} + [var=index_question_4]")])
all_images.extend(images)

for image_file in glob.glob(f"{imgage_folder_path}{os.sep}*"):
    os.remove(image_file)

for image in all_images:
    file_name, image_data, timestamp = image
    with open(f"{imgage_folder_path}{os.sep}{file_name}", "wb+") as f:
        f.write(base64.b64decode(image_data))

#format_images_to_xml(folder_path, all_images)
