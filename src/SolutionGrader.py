import numpy as np
from abc import ABC, abstractmethod
from typing import Tuple


class SolutionGraderInterface(ABC):
    """
    Klasa reprezentująca interfejs oceniania otrzymanego rozwiązania
    """
    @abstractmethod
    def grade_solution(self, solution: np.array, clients_map: np.array):
        raise NotImplementedError


class SolutionGrader(SolutionGraderInterface):
    """
    Klasa zawierająca funkcjonalności związane z oceną rozwiązania ostatecznego pod względem dodatkowych kryteriów.
    """
    def __init__(self,
                 clients_map: np.array,
                 solution: np.array):

        self.__clients_map = clients_map
        self.__solution = solution
        self.__map_shape = self.__clients_map.shape

    def grade_solution(self, solution: np.array, clients_map: np.array):
        """
        Funkcja oceniająca rozwiązanie pod dodatkowym kryterium.

        :param solution: rozwiązanie do oceny pod dodatkowym kryterium
        :param clients_map: mapa klientów służąca do oceny
        :return:
        """
        self.__solution = solution
        self.__clients_map = clients_map

        clients_per_pl = self.__map_clients_to_nearest_pl()

        return np.var(clients_per_pl[clients_per_pl > 0])

    def __map_clients_to_nearest_pl(self) -> np.array:
        """
        Funkcja licząca ile klientów ma najbliżej do danej stacji dokującej.

        :return nearest_clients_no: macierz, gdzie w miejscu stacji dokujących wpisana jest ilość klientów,
                                    którzy mają do niego najbliżej
        """
        nearest_clients_no = np.zeros(self.__map_shape)
        for x in range(self.__clients_map.shape[0]):
            for y in range(self.__clients_map.shape[1]):
                if self.__clients_map[x, y] > 0:
                    nearest_clients_no[self.__find_nearest_pl((x, y))] += self.__clients_map[x, y]

        return nearest_clients_no

    def __find_nearest_pl(self, clients_cell_coords: Tuple[int, int]) -> Tuple[int, int]:
        """
        Funkcja znajdująca najbliższą stację dokującą dla danej komórki z klientami.

        :param clients_cell_coords:  współrzędne komórki z klientami, dla których szukamy najbliższej stacji dokującej
        :return nearest_pl: współrzędne najbliższej stacji dokującej
        """
        cx, cy = clients_cell_coords
        
        max_dst_to_left = cx
        max_dst_to_right = self.__map_shape[0] - cx - 1
        max_dst_to_up = cy
        max_dst_to_down = self.__map_shape[1] - cy - 1

        max_search_rad = np.max([max_dst_to_left + max_dst_to_up,
                                 max_dst_to_left + max_dst_to_down,
                                 max_dst_to_right + max_dst_to_down,
                                 max_dst_to_right + max_dst_to_up])

        for search_rad in range(max_search_rad + 1):
            for x in range(cx - search_rad, cx + search_rad + 1):
                diff = search_rad - np.abs(x - cx)
                y_min = cy - diff
                y_max = cy + diff
                for y in [y_min, y_max]:
                    if 0 <= x <= self.__map_shape[0] - 1 and 0 <= y <= self.__map_shape[1] - 1:
                        if np.abs(cx - x) + np.abs(cy - y) == search_rad and self.__solution[x, y] == 1:
                            return x, y
