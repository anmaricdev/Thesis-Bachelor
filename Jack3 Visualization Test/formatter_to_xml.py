import os
import xml.etree.ElementTree as ET

def clear_variable_declarations(folder_path):
    """Clear any existing variable declarations in the folder."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def format_to_xml(folder_path, result, question_number, num_calls, image_ids):
    """Format the results to XML format."""
    root = ET.Element("question")
    root.set("number", str(question_number))
    
    # Add results
    for var_name, var_single, content in result:
        var_elem = ET.SubElement(root, "variable")
        var_elem.set("name", var_name)
        var_elem.set("single", var_single)
        var_elem.text = content
    
    # Add image IDs
    for id_name, id_value in image_ids:
        id_elem = ET.SubElement(root, "image_id")
        id_elem.set("name", id_name)
        id_elem.text = id_value
    
    # Create XML file
    tree = ET.ElementTree(root)
    xml_path = os.path.join(folder_path, f"question_{question_number}.xml")
    tree.write(xml_path, encoding='utf-8', xml_declaration=True) 