import numpy as np
from abc import ABC, abstractmethod
from typing import Tuple


class ProblemGenInterface(ABC):
    """
    Interfejs klas realizujących generowanie problemu do rozwiązania
    """
    @abstractmethod
    def __init__(self,

                 map_shape: Tuple[int, int],
                 clients_number: int,
                 max_clients_number_in_cell: int):
        pass

    @abstractmethod
    def generate_problem(self) -> np.array:
        pass


class RandomProblemGen(ProblemGenInterface):
    """
    Klasa realizująca interfejs generatora problemów.
    Generuje macierz klientów w sposób losowy
    """
    def __init__(self,

                 map_shape: Tuple[int, int],
                 clients_number: int,
                 max_clients_number_in_cell: int):

        self.__map_shape = map_shape
        self.__clients_number = clients_number
        self.__max_clients_number_in_cell = max_clients_number_in_cell

    def generate_problem(self) -> np.array:

        # wygeneruj początkową macierz losową o zadanym rozmiarze, minimalnej wartości komórki 0 i maksymalnej
        # równej self.__max_clients_number_in_cell
        problem_matrix = np.random.randint(0, self.__max_clients_number_in_cell, self.__map_shape)

        # jeśli sumaryczna ilość klientów na mapie jest za duża
        if np.sum(problem_matrix) > self.__clients_number:
            for _ in range(np.sum(problem_matrix) - self.__clients_number):
                # sprawdź, ile jest elementów większych od zera
                cell_with_clients = problem_matrix > 0
                cell_with_clients_no = np.count_nonzero(cell_with_clients)
                # wylosuj indeks (numer) komórki do pomniejszenia o 1
                # jeśli zamiast indeksów do nawiasów kwadratowych macierzy numpy
                # wstawimy macierz o elementach True, False to zwróci nam to wektor
                # [o wymiarze (,rozmiar_wektora) - dlatego argumentem dla np.zeros jest liczba a nie krotka]
                # o elementach, niestety nie możemy potem odwołać się do tego wektora
                # tylko musimy stosować dziwną konstrukcję z dodatkowym wektorem z jedną jedynką
                index_to_sub_1 = np.random.randint(0, cell_with_clients_no - 1)
                # trzeba zmienić typ macierzy, żeby dało się odjąć
                to_sub1 = np.zeros(cell_with_clients_no, dtype='int32')
                to_sub1[index_to_sub_1] = 1
                problem_matrix[cell_with_clients] -= to_sub1

        # jeśli sumaryczna ilość klientów na mapie jest za mała
        else:
            for _ in range(self.__clients_number - np.sum(problem_matrix)):
                # sprawdź, ile jest elementów mniejszych od maksymalnej ilości klientów w komórce
                cell_with_less_clients = problem_matrix < self.__max_clients_number_in_cell
                cell_with_less_clients_no = np.count_nonzero(cell_with_less_clients)
                # wylosuj indeks (numer) komórki do powiększenia o 1
                # jeśli zamiast indeksów do nawiasów kwadratowych macierzy numpy
                # wstawimy macierz o elementach True, False to zwróci nam to wektor
                # [o wymiarze (,rozmiar_wektora) - dlatego argumentem dla np.zeros jest liczba a nie krotka]
                # o elementach, niestety nie możemy potem odwołać się do tego wektora
                # tylko musimy stosować dziwną konstrukcję z dodatkowym wektorem z jedną jedynką
                index_to_sub_1 = np.random.randint(0, cell_with_less_clients_no - 1)
                # trzeba zmienić typ macierzy, żeby dało się dodać
                to_add1 = np.zeros(cell_with_less_clients_no, dtype='int32')
                to_add1[index_to_sub_1] = 1
                problem_matrix[cell_with_less_clients] += to_add1

        return problem_matrix


if __name__ == '__main__':
    p_gen = RandomProblemGen(map_shape=(1, 1),
                             clients_number=1,
                             max_clients_number_in_cell=1)
