import os

def get_output_directory():
    base_path = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_path, '../output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir
