import random
from formatter_for_copy_paste_export_to_jack3 import *
from formatter_to_xml import format_to_xml, clear_variable_declarations
from append_question_number_to_string import append_question_number_to_string

def generate_solution_regex(answer: str) -> str:
    solution = answer
    solution = solution.replace(" ", "").replace(",", r"\s*,\s*").replace("[", r"\[*\s*").replace("]", r"\s*\]*")
    solution = fr"\[*\s*{solution}\s*\]*"
    return f"{solution}"

def bin_packing_show_the_packing_exercise(question_number, num_calls, algorithm):
    import matplotlib.pyplot as plt
    from Visualization import visualize_bin_packing
    from BinPackingAlgorithms import (
        bin_packing_best_fit_var_capa,
        bin_packing_first_fit_var_capa,
        bin_packing_next_fit_var_capa,
        bin_packing_worst_fit_var_capa
    )
    import os
    import base64

    # Parameters for random generation
    min_bin_count, max_bin_count = 2, 5
    min_bin_capacity, max_bin_capacity = 8, 15
    min_item_count, max_item_count = 8, 12
    min_item_size, max_item_size = 1, 8

    arrays = []
    bin_capacities_list = []
    solutions = []
    solutions_regexes = []
    image_filenames = []

    for i in range(num_calls):
        # Generate random bins and items
        bin_count = random.randint(min_bin_count, max_bin_count)
        bin_capacities = [random.randint(min_bin_capacity, max_bin_capacity) for _ in range(bin_count)]
        item_count = random.randint(min_item_count, max_item_count)
        items = [random.randint(min_item_size, max_item_size) for _ in range(item_count)]

        # Compute solution using the specified algorithm
        if algorithm == "BEST":
            _, bins, _ = bin_packing_best_fit_var_capa(bin_capacities.copy(), items.copy())
        elif algorithm == "FIRST":
            _, bins, _ = bin_packing_first_fit_var_capa(bin_capacities.copy(), items.copy())
        elif algorithm == "NEXT":
            _, bins, _ = bin_packing_next_fit_var_capa(bin_capacities.copy(), items.copy())
        elif algorithm == "WORST":
            _, bins, _ = bin_packing_worst_fit_var_capa(bin_capacities.copy(), items.copy())
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        # Only include non-empty bins for the solution
        solution = [b for b in bins if b]

        # Generate regex for the solution
        solution_str = str(solution)
        solution_regex = generate_solution_regex(",".join(["[" + ",".join(map(str, b)) + "]" for b in solution]))

        # Save the image
        fig = visualize_bin_packing(bin_capacities, items, visualize_in_2d=False, algorithms=[algorithm])
        image_filename = f"Exercise_{question_number}_variant_{i+1}.png"
        image_path = os.path.join(folder_path, image_filename)
        fig.savefig(image_path, format='png', bbox_inches='tight', pad_inches=0, dpi=150)
        plt.close(fig)

        arrays.append(items)
        bin_capacities_list.append(bin_capacities)
        solutions.append(solution)
        solutions_regexes.append(solution_regex)
        image_filenames.append(image_filename)

    return [
        (append_question_number_to_string(question_number, 'bin_capacities'), append_question_number_to_string(question_number, 'bin_capacity'), format_list_of_arrays(bin_capacities_list)),
        (append_question_number_to_string(question_number, 'items'), append_question_number_to_string(question_number, 'item'), format_list_of_arrays(arrays)),
        (append_question_number_to_string(question_number, 'solutions'), append_question_number_to_string(question_number, 'solution'), format_list_of_strings(solutions)),
        (append_question_number_to_string(question_number, 'solution_regexes'), append_question_number_to_string(question_number, 'solution_regex'), format_list_of_strings(solutions_regexes)),
        (append_question_number_to_string(question_number, 'image_filenames'), append_question_number_to_string(question_number, 'image_filename'), format_list_of_strings(image_filenames))
    ]

# Wichtig: Hier soll der Pfad angegeben werden von dem Ordner, wo die XML drin ist. Nicht der Pfad zu der XML selbst.
folder_path = r"/Users/antemaric/Desktop/Bachelorarbeit/Thesis-Bachelor/Exercises"

clear_variable_declarations(folder_path)

num_calls = 5

question_number = 1
algorithm = "BEST"
result = bin_packing_show_the_packing_exercise(question_number, num_calls, algorithm)
format_to_xml(
    folder_path,
    result,
    question_number,
    num_calls,
    [
        ("image_ids_start", "Put image start id here"),
        (f"question_{question_number}_image_id", f"[var=image_ids_start] + {str(num_calls*(question_number-1))} + [var=index_question_{question_number}]")
    ]
)

question_number = 2
algorithm = "FIRST"
result = bin_packing_show_the_packing_exercise(question_number, num_calls, algorithm)
format_to_xml(
    folder_path,
    result,
    question_number,
    num_calls,
    [
        (f"question_{question_number}_image_id", f"[var=image_ids_start] + {str(num_calls*(question_number-1))} + [var=index_question_{question_number}]")
    ]
)

"""
Step-by-step:
1. Aufgabe in JACK erstellen (kann auch leere Aufgabe sein)
2. Aufgabe aus JACK exportieren
3. Python Skript für diese Aufgabe anlegen
    - Sicherstellen, dass formatter_to_xml.py, etc. zugriffbar sind.
    - folder_path setzen
    - Methode für Generierung der Aufgaben schreiben
    - Benötigte Funktionen callen
4. Python Skript ausführen
5. Veränderte XML in JACK importieren
6. Bilder hochladen (in korrekter Reihenfolge)
    - Erst Aufgabe 1, Bild 1
    - Dann Aufgabe 1, Bild 2
    - etc.
7. Die allererste ID von den Bildern kopieren und in die Variable "image_ids_start" abspeichern
8. Bilder und Eingaben, etc. in Aufgabenbeschreibung/Feedback hinzufügen
9. Sicherstellen, dass alles klappt!
"""
