import sys
import os

# This should be used for every file in a map
def add_project_path():
    script_dir = os.path.dirname(__file__)  # De map waar path_helper.py staat
    project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))  # De rootmap van je project
    src_folder = os.path.join(project_root, 'src')
    
    if src_folder not in sys.path:
        sys.path.append(src_folder)