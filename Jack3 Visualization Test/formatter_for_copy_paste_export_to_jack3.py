def format_list_of_arrays(arrays):
    """Format a list of arrays into a string representation."""
    return '\n'.join([format_array(arr) for arr in arrays])

def format_array(arr):
    """Format a single array into a string representation."""
    return '[' + ', '.join(map(str, arr)) + ']'

def format_list_of_strings(strings):
    """Format a list of strings into a string representation."""
    return '\n'.join(strings) 