import numpy as np
from abc import ABC, abstractmethod
from typing import Tuple

import src.Helpers as Helpers


class StartingSolutionGenInterface(ABC):

    @abstractmethod
    def __init__(self,
                 n_max: int,
                 p_max: int,
                 d_max: int,

                 clients_map: np.array):
        pass

    @abstractmethod
    def generate(self) -> np.array:
        raise NotImplementedError
        pass


class StartingSolutionGen(StartingSolutionGenInterface):

    def __init__(self,
                 n_max: int,
                 p_max: int,
                 d_max: int,

                 clients_map: np.array):

        self.__n_max = n_max
        self.__p_max = p_max
        self.__d_max = d_max

        self.__client_map = clients_map
        self.__map_shape = self.__client_map.shape
        self.__temp_clients_map = np.copy(self.__client_map)

        self.__mask_matrix = np.zeros(self.__map_shape)

        self.__diamond_matrix = Helpers.diamond(self.__d_max)

    def generate(self) -> np.array:

        self.__temp_clients_map = np.copy(self.__client_map)
        starting_solution = np.zeros(self.__map_shape, dtype='int32')

        available_pl = self.__n_max

        while available_pl > 0:
            self.__make_mask_matrix()
            place_found = False

            while not place_found:

                if np.max(self.__mask_matrix) == -1:
                    raise RuntimeError("Can't generate starting solution")

                max_ind = np.unravel_index(np.argmax(self.__mask_matrix, axis=None), self.__mask_matrix.shape)

                if self.__check_client_number_in_pl_range(max_ind) > self.__p_max or starting_solution[max_ind] == 1:


                    self.__mask_matrix[max_ind] = -1
                else:
                    starting_solution[max_ind] = 1
                    available_pl -= 1
                    place_found = True
                    self.__reduce_temp_clients_map(max_ind)

        return starting_solution

    def __reduce_temp_clients_map(self, cell_coord: Tuple[int, int]):

        y, x = cell_coord
        r = self.__d_max

        x_min = x - r if x - r > 0 else 0
        x_max = x + r + 1 if x + r + 1 < self.__map_shape[1] else self.__map_shape[1]
        y_min = y - r if y - r > 0 else 0
        y_max = y + r + 1 if y + r + 1 < self.__map_shape[0] else self.__map_shape[0]

        mx_min = r - (x - x_min)
        mx_max = r + (x_max - 1 - x) + 1
        my_min = r - (y - y_min)
        my_max = r + (y_max - 1 - y) + 1

        temp_temp_clients_map = np.copy(self.__temp_clients_map[y_min:y_max, x_min:x_max])
        temp_temp_clients_map[self.__diamond_matrix[my_min:my_max, mx_min:mx_max]] = 0

        self.__temp_clients_map[y_min:y_max, x_min:x_max] = temp_temp_clients_map

    def __make_mask_matrix(self):

        self.__mask_matrix = np.zeros(self.__map_shape)
        r = self.__d_max
        for index, value in np.ndenumerate(self.__temp_clients_map):
            if value > 0:
                y, x = index

                x_min = x - r if x - r > 0 else 0
                x_max = x + r + 1 if x + r + 1 < self.__map_shape[1] else self.__map_shape[1]
                y_min = y - r if y - r > 0 else 0
                y_max = y + r + 1 if y + r + 1 < self.__map_shape[0] else self.__map_shape[0]

                mx_min = r - (x - x_min)
                mx_max = r + (x_max - 1 - x) + 1
                my_min = r - (y - y_min)
                my_max = r + (y_max - 1 - y) + 1

                temp_mask = np.copy(self.__mask_matrix[y_min:y_max, x_min:x_max])
                temp_mask[self.__diamond_matrix[my_min:my_max, mx_min:mx_max]] += 1

                self.__mask_matrix[y_min:y_max, x_min:x_max] = temp_mask

    def __check_client_number_in_pl_range(self, pl_coords: Tuple[int, int]) -> int:

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

        clients_sum = np.sum(
            self.__client_map[y_min:y_max, x_min:x_max][self.__diamond_matrix[my_min:my_max, mx_min:mx_max]])

        return int(clients_sum)


if __name__ == "__main__":
    s_gen = StartingSolutionGen(n_max=1,
                                p_max=1,
                                d_max=1,

                                clients_map=np.array([1]))
