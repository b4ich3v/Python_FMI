import importlib.util
import os

X = 73

def find_file(filename, search_path):
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

file_path = find_file('info.py', os.getcwd())

if file_path:
    spec = importlib.util.spec_from_file_location("info", file_path)
    info = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(info)
    X = info.POSITION + 1
else:
    print("Error")
