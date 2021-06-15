import sys
import os


def is_path_to_file_exists(_path_to_file: str) -> bool:

    dir = os.path.dirname(_path_to_file)
    return os.path.exists(dir)


def generate_path_to_file(_path_to_file: str):

    dir = os.path.dirname(_path_to_file)
    os.makedirs(dir)


if __name__ == '__main__':

    path_to_file = '../plots/test/file'
    if not is_path_to_file_exists(path_to_file):
        generate_path_to_file(path_to_file)
    sys.exit(0)