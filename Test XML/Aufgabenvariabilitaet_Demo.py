import random
from formatter_for_copy_paste_export_to_jack3 import *
from formatter_to_xml import format_to_xml, clear_variable_declarations
from append_question_number_to_string import append_question_number_to_string

def generate_solution_regex(answer: str) -> str:
    solution = answer
    solution = solution.replace(" ", "").replace(",", r"\s*,\s*").replace("[", r"\[*\s*").replace("]", r"\s*\]*")
    solution = fr"\[*\s*{solution}\s*\]*"
    return f"{solution}"

def tree_traversal_test(question_number, num_calls):
    ARRAY_SIZE = 4
    arrays = []
    for _ in range(num_calls):
        array = []
        for _ in range(ARRAY_SIZE):
            array.append(random.randint(0, 9))
        arrays.append(array)

    solutions = list(map(lambda arr: list(reversed(arr)), arrays))
    solutions_regexes = list(map(lambda sol: generate_solution_regex(",".join(map(str, sol))), solutions))
    return [
        (append_question_number_to_string(question_number, 'arrays'), append_question_number_to_string(question_number, 'array'), format_list_of_arrays(arrays)),
        (append_question_number_to_string(question_number, 'solutions'), append_question_number_to_string(question_number, 'solution'), format_list_of_strings(solutions)),
        (append_question_number_to_string(question_number, 'solution_regexes'), append_question_number_to_string(question_number, 'solution_regex'), format_list_of_strings(solutions_regexes))
    ]

# Wichtig: Hier soll der Pfad angegeben werden von dem Ordner, wo die XML drin ist. Nicht der Pfad zu der XML selbst.
folder_path = r"path/to/directory/containing/xml"

clear_variable_declarations(folder_path)

num_calls = 5

question_number = 1
result = tree_traversal_test(question_number, num_calls)
format_to_xml(folder_path, result, question_number, num_calls, [("image_ids_start", "Put image start id here"), ("question_1_image_id", f"[var=image_ids_start] + {str(num_calls*(question_number-1))} + [var=index_question_1]")])

question_number = 2
result = tree_traversal_test(question_number, num_calls)
format_to_xml(folder_path, result, question_number, num_calls, [("question_2_image_id", f"[var=image_ids_start] + {str(num_calls*(question_number-1))} + [var=index_question_2]")])

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
