import sys
import os
"""
    Zbiór funkcji odpowiedzialnych za zarządzanie plikami, sprawdzanie istanienia czy istnieje dana ścieżka oraz
    generowanie zadanej ścieżki.
    
"""


def is_path_to_file_exists(_path_to_file: str) -> bool:
    """
    Sprawdza czy istnieje scieżka do katalogu gdzie ma zostać zapisany dany plik
    :param _path_to_file: Scieżka do pliku
    :return: TRUE - scieżka istnieje, FALSE - gdy scieżka nie istnieje
    """
    dir = os.path.dirname(_path_to_file)
    return os.path.exists(dir)


def generate_path_to_file(_path_to_file: str):
    """
    Generuje ścieżke do katalogu gdzie ma być zapisany plik
    :param _path_to_file:
    :return:
    """
    dir = os.path.dirname(_path_to_file)
    os.makedirs(dir)


if __name__ == '__main__':
    """
        Przykładowe użycie powyższych funkcji
    """
    path_to_file = '../plots/test/file'
    if not is_path_to_file_exists(path_to_file):
        generate_path_to_file(path_to_file)
    sys.exit(0)