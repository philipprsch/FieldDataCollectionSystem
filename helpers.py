import ujson
import sys
import uos

def read_json(file_path):
    try:
        with open(file_path, 'r') as file:
            # Load and parse the JSON content into a Python dictionary
            data = ujson.load(file)
            return data
    except OSError as e:
        print(f"Error opening file: {e}")
        return None
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
        return None
def is_module_imported(module_name):
    # Check if the module is already in sys.modules
    return module_name in sys.modules

def dynamic_import(module_name):
    # Dynamically import the module
    if is_module_imported(module_name):
        print(f"Module '{module_name}' is already imported.")
        return None
    try:
        module = __import__(module_name)
        print(f"Module '{module_name}' imported successfully.")
        return module
    except ImportError:
        print(f"Failed to import module '{module_name}'.")


#Helper functions for file manipulation
def does_folder_exist(directory):
    # Try listing the contents of the directory
    try:
        uos.listdir(directory)
        return True  
    except OSError:
        return False  
    
def append_to_file(filename, data):
    with open(filename, "a") as file:  # 'a' mode for appending
        file.write(data)
        print(f"Data '{data}' appended to {filename}")

# Read from file
def read_file(filename):
    try:
        with open(filename, "r") as file:
            content = file.read()
            print(f"Contents of {filename}:")
            print(content)
            return content
    except OSError:
        print(f"{filename} does not exist yet.")
        return ""
