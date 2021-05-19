import numpy as np
from abc import ABC, abstractmethod
from typing import Tuple

import src.Helpers as Helpers


class ConditionTesterInterface(ABC):
    """
    Interfejs klasy sprawdzającej ograniczenia
    """

    @abstractmethod
    def __init__(self,
                 p_max: int,
                 d_max: int,

                 clients_map: np.array):
        pass

    @abstractmethod
    def is_solution_allowed(self, solution: np.array) -> bool:
        raise NotImplementedError
        pass


class OneConditionTester(ConditionTesterInterface):
    """
    Klasa realizująca interfejs klasy sprawdzającej ograniczenia
    """

    def __init__(self,
                 p_max: int,
                 d_max: int,

                 clients_map: np.array):
        """
        :param p_max: maksymalna liczba klientów w zasięgu działania stacji dokującej
        :param d_max: zasięg działania stacji dokujących
        :param clients_map: macierz zawierająca informacje o położeniu klientów
        """
        self.__p_max = p_max
        self.__d_max = d_max
        self.__clients_map = clients_map

        self.__map_shape = self.__clients_map.shape

        self.__mask = Helpers.diamond(self.__d_max)

        self.__ban_matrix = self.__create_ban_matrix()

    def is_solution_allowed(self, solution: np.array) -> bool:
        """
        Metoda sprawdzająca, czy dane rozwiązanie spełnia ograniczenia.

        :param solution: rozwiązanie do przetestowania pod względem ograniczeń
        :return [bool]: odpowiedź na pytanie, czy dane rozwiązanie spełnia ograniczenia
        """

        return not np.any(solution[self.__ban_matrix])

    def __create_ban_matrix(self) -> np.array:
        """
        Tworzy macierz logiczną, gdzie True oznacza miejsca, gdzie nie można postawić stacji dokujących
        :return ban_matrix: macierz wskazująca gdzie nie można postawić stacji dokujących
        """
        ban_matrix = np.zeros(self.__map_shape, dtype=bool)
        for index, value in np.ndenumerate(ban_matrix):
            ban_matrix[index] = self.__are_to_many_clients_in_area(index)
        return ban_matrix

    def __are_to_many_clients_in_area(self, pl_coords: Tuple[int, int]) -> bool:
        """
        FUnkcja sprawdzająca, czy w zasięgu działa stacji dokujących o współrzędnych pl_coords
        nie ma zbyt wielu klientów.

        :param pl_coords: współrzędne stacji dokujących
        :return [bool]: czy w zasięgu stacji dokujących nie ma zbyt wielu klientów
        """

        y, x = pl_coords
        r = self.__d_max

        x_min = x - r if x - r > 0 else 0
        x_max = x + r + 1 if x + r + 1 < self.__map_shape[1] else self.__map_shape[1]
        y_min = y - r if y - r > 0 else 0
        y_max = y + r + 1 if y + r + 1 < self.__map_shape[0] else self.__map_shape[0]

        mx_min = r - (x - x_min)
        mx_max = r + (x_max - 1 - x) + 1
        my_min = r - (y - y_min)
        my_max = r + (y_max - 1 - y) + 1

        total_clients_in_area = np.sum(
            self.__clients_map[y_min:y_max, x_min:x_max][self.__mask[my_min:my_max, mx_min:mx_max]])

        return total_clients_in_area > self.__p_max


if __name__ == '__main__':
    cond = OneConditionTester(p_max=1,
                              d_max=1,

                              clients_map=np.array([1]))
