import numpy as np
from abc import ABC, abstractmethod
from typing import Tuple

import src.Helpers as Helpers


class StartingSolutionGenInterface(ABC):
    """
    Interfejs generatora rozwiązania początkowego
    """

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
    """
    Implementacja interfejsu generatora.

    Idea działania:

    Otrzymujemy macierz z ilością klienktów w każdej komórce.
    Tworzymy drugą macierz wypełnioną zerami o takich samych rozmiarach
    Nakładamy maski na tę drugą macierz
    Maski składają się z kul w naszej metryce o promieniu 2*D_max+1 wypełnionych jedynkami
    Środek maski odpowiada pozycji kratki z klientami dla której są nakładane
    Gdzie maski się pokrywają, tam wartość drugiej macierzy jest sumą tych masek

    Przykład dla D_max=2:
    Macierz wejściowa:
    |3 0 0 0 2|
    |0 0 1 0 0|
    |0 2 0 0 0|
    |0 0 0 1 1|

    Macierz nałożonych masek: - kształt masek zależy od metryki
    |1 2 3 2 1|
    |2 3 2 2 2|
    |2 2 3 4 2|
    |1 2 3 2 2|

    Algorym wyszukiwania rozwiązania początkowego działa tak,
    że wybierana jest komórka z największą wartością (jeśli jest kilka to sposób wyboru jest bez znaczenia)
    Następnie zerowane są wszystie komórki w odległości D_max od danej komórki (w metryce nakładania maski)
    Tak uzyskaną macierz ponownie wkładam do funkcji i otrzymujemy kolejne położenie paczkomatu

    Kryterium stopu: skończyły się paczkomaty

    Jeśli pozostały paczkomaty, a miejsca do ich umieszczenia nie ma (wszystkie pozostałe komórki
    nie spełniają ograniczeń) to rzucany jest wyjątek, że nie można wygenerować rozwiązania początkowego
    """

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
        """
        Metoda generująca rozwiązanie początkowe.
        # jeśli zmieniamy nasze ograniczenia to musimy zmodyfikować ConditionTester oraz tę klasę !!!

        :return starting_solution: rozwiązanie początkowe spełniające ograniczenia
        """
        self.__temp_clients_map = np.copy(self.__client_map)
        starting_solution = np.zeros(self.__map_shape, dtype='int32')

        available_pl = self.__n_max

        while available_pl > 0:
            self.__make_mask_matrix()
            place_found = False
            # iteruje po komórkach o wartościach od największych do najmniejszych, aż nie znajdzie optymalnego miejsca
            while not place_found:
                # jeśli przeszukano wszystkie pozycje i nie znaleziono miejsca
                if np.max(self.__mask_matrix) == -1:
                    raise RuntimeError("Can't generate starting solution")
                # znajduje pierwsze maksimum w macierzy masek
                max_ind = np.unravel_index(np.argmax(self.__mask_matrix, axis=None), self.__mask_matrix.shape)

                if self.__check_client_number_in_pl_range(max_ind) > self.__p_max or starting_solution[max_ind] == 1:
                    # wstawiam -1, żeby maksimum mi nie znajdowało tej komórki (zabraniam ustawienia paczkomatu
                    # w to miejsce) jeśli max to będzie -1, to wtedy generator kończy działanie
                    self.__mask_matrix[max_ind] = -1
                else:
                    starting_solution[max_ind] = 1
                    available_pl -= 1
                    place_found = True
                    self.__reduce_temp_clients_map(max_ind)

        return starting_solution

    def __reduce_temp_clients_map(self, cell_coord: Tuple[int, int]):
        """
        Usuwa klientów w tymczasowej mapie po wstawieniu w okolicy paczkomatu

        :param cell_coord: współrzędne punktu, którego otoczenia w mapie klientów ma być zredukowane
        :return:
        """
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
        """
        Funkcja tworząca macierz maskową.

        :return: None
        """
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
        """
        Liczy liczbę klientów w zasięgu danego paczkomatu

        :param pl_coords: współrzędne paczkomatu
        :return clients_number: liczba klientów w zasięgu danego paczkomatu
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

        clients_sum = np.sum(
            self.__client_map[y_min:y_max, x_min:x_max][self.__diamond_matrix[my_min:my_max, mx_min:mx_max]])

        return int(clients_sum)


if __name__ == "__main__":
    s_gen = StartingSolutionGen(n_max=1,
                                p_max=1,
                                d_max=1,

                                clients_map=np.array([1]))
