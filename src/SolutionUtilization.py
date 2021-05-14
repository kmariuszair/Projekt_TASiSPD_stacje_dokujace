import numpy as np
import matplotlib.pyplot as plt
import logging

from src.PlotSaver import save_plot_to_file
import src.Helpers as Helpers
"""
    Klasa służąca do oblicznia wykorzystania paczkomatów oraz reprezentacji graficznej obciążenia
"""


class SolutionUtilization:

    def __init__(self, _client_map: np.array, _solution: np.array, _p_max: int, _d_max: int):
        """
        :param _client_map: Mapa klientów
        :param _solution: Rozmieszczenie paczkomatów
        :param _p_max: Maksymalna pojemność pojedynczego paczkomatu
        :param _d_max: Zasięg działania paczkomatu
        """
        self.__client_map = np.copy(_client_map)
        self.__plt_map = np.copy(_solution)
        self.__p_max = _p_max
        self.__d_max = _d_max
        self.__map_shape = self.__client_map.shape
        # Macierz reprezentująca czy klient jest w strefie działania paczkomatu
        self.__client_within_plt_zone = np.zeros(self.__map_shape)
        # Macierz reprezentująca ile klientów ma w zasięgu działania dany paczkomat
        # 1 - Klient jest W zasiegu paczkomatu
        # 0 - Klient jest POZA zasiegiem paczkomatu
        self.__plt_utilisation = np.zeros(self.__map_shape)
        # Macierz reprezentująca ile klientów ma paczkomat bez ograniczeń
        self.__plt_utilisation_without_d_max = np.zeros(self.__map_shape)

        # Lista przedstawiająca średnią odległość komórki od paczkomatu w zależności od ilości klientów w tej komórce.
        # Liczba klientów jest indeksem
        self.__av_distance_for_clients_cell = dict()
        # Średnia liczba klientów w zależności od odległosci od paczkomatu
        self.__av_clients_at_given_range = dict()
        # Macierz odległości do najbliższego paczkomatu. Wartość komórki określa jej oddalenie od najbliższego
        # paczkomatu
        self.__distance_matrix = np.zeros(self.__map_shape)

        # Wygeneruj dla danych wejściowych macierze obciążenia paczkomatów, stref działania itp
        self.__calculate()

    def calculate_utilization_of_solution(self, _client_map: np.array, _plt_map: np.array, _p_max: int, _d_max: int):
        """
        Funckja służaca do ponownego generowania rozwiązania zużycia paczkomatów
        :param _client_map: Mapa klientów
        :param _plt_map: Rozmieszczenie paczkomatów
        :param _p_max: Maksymalna pojemność pojedynczego paczkomatu
        :param _d_max: Maksymalny zasięg działania paczkomatu
        :return: Funkcja wewnętrzenie zapisuje rozwiązanie pod zmienna self.__plt_utilisation_without_d_max
        """
        self.__client_map = np.copy(_client_map).T
        self.__plt_map = np.copy(_plt_map).T
        self.__p_max = _p_max
        self.__d_max = _d_max
        self.__map_shape = self.__client_map.shape
        self.__plt_utilisation_without_d_max = np.zeros(self.__map_shape).T
        # Przelicz ponownie rozwiązanie dla nowych danych wejściowych
        self.__calculate()

    def plot_solution_utilization(self):
        """
            Funkcja reprezentująca wykorzystanie paczkomatów w zasięgu ich działania
        """
        fig = plt.figure(figsize=(16, 12))
        ax = fig.add_subplot(111)
        im = ax.imshow(self.__plt_utilisation, origin='lower', interpolation='None', cmap='Reds')
        plt.xlabel('Pozycja osi X')
        plt.ylabel('Pozycja osi Y')
        plt.title('Wykorzystanie poszczególnych paczkomatów w zasięgu ich działania')
        size = self.__plt_utilisation.shape
        for (j, i), label in np.ndenumerate(self.__plt_utilisation):
            if int(label) != 0 and self.__plt_map[j][i]:
                ax.text(i, j, int(label), ha='center', va='center')
        plt.xticks(range(0, size[1]))
        plt.yticks(range(0, size[0]))
        fig.colorbar(im)
        save_plot_to_file(plt, 'Dystrybucja klientow do paczkomatow')
        plt.show()

    def plot_clients_within_plt_zone(self):
        """
            Funkcja służąca do reprezentacji graficznej obszaru obsługiwanego przez paczkomaty
        """
        fig = plt.figure(figsize=(16, 12))
        ax = fig.add_subplot(111)
        im = ax.imshow(self.__client_within_plt_zone, origin='lower', interpolation='None', cmap='cool')
        plt.xlabel('Pozycja osi X')
        plt.ylabel('Pozycja osi Y')
        plt.title('Zasięg działania paczkomatów')
        size = self.__client_within_plt_zone.shape
        for (j, i), label in np.ndenumerate(self.__client_map):
            if self.__plt_map[j][i]:
                plt.plot(i, j, 'wo')
        plt.xticks(range(0, size[1]))
        plt.yticks(range(0, size[0]))
        save_plot_to_file(plt, 'Zasieg dzialania paczkomatow')
        plt.show()

    def plot_solution_utilization_without_d_max(self):
        """
            Funkcja reprezentująca wykorzystanie paczkomatów BEZ zasięgu ich działania
        """
        fig = plt.figure(figsize=(16, 12))
        ax = fig.add_subplot(111)
        im = ax.imshow(self.__plt_utilisation_without_d_max, origin='lower', interpolation='None', cmap='YlOrBr')
        plt.xlabel('Pozycja osi X')
        plt.ylabel('Pozycja osi Y')
        plt.title('Wykorzystanie poszczególnych paczkomatów bez ograniczeń odległościowych')
        size = self.__plt_utilisation_without_d_max.shape
        for (j, i), label in np.ndenumerate(self.__plt_utilisation_without_d_max):
            if int(label) != 0 and self.__plt_map[j][i]:
                ax.text(i, j, int(label), ha='center', va='center')
        plt.xticks(range(0, size[1]))
        plt.yticks(range(0, size[0]))
        fig.colorbar(im)
        save_plot_to_file(plt, 'Dystrybucja klientow do paczkomatow BEZ ograniczenia ')
        plt.show()

    def get_plt_utilization_without_d_max(self):
        """
        Funkcja wzracająca kopię mapy wykorzystania paczkomatów bez ograniczenia odległościowego
        :return: Macierz wykorzystania paczkomatów bez ograniczenia odległościowego
        """
        return np.copy(self.__plt_utilisation_without_d_max)

    def get_plt_utilization(self):
        """
        Funkcja wzracająca kopię mapy wykorzystania paczkomatów
        :return: Macierz wykorzystania paczkomatów
        """
        return np.copy(self.__plt_utilisation)

    def print_solution_utilization_data(self):
        """
            Funkcja wypisująca w konsoli informacje zebrane podczas działania algorytmu
            Reprezentowane są następujące informacje:
                - Ile klientow nie ma dostępu do poczkomatów, ile stanowi to całość populacji
                - Mediana, średnie obciążenie paczkomatów, zużycie całkowitej pojemności
        """
        #  Wyświetlanie informacji o klientach bez dostępu do paczkomatów
        logging.info('>------      Informacje o uzyskanym rozwiązaniu      ------<')
        total_clients_without_plt = 0
        zones_without_plt = 0
        for (j, i), value in np.ndenumerate(self.__client_within_plt_zone):
            if value == 0:
                total_clients_without_plt += self.__client_map[j][i]
                zones_without_plt += 1
        total_clients = np.sum(self.__client_map)
        total_client_info = 'Liczba klientów bez dostępu do paczkomatów wynosi: {}'.format(total_clients_without_plt)
        logging.info(total_client_info)
        total_client_percent = float(total_clients_without_plt/total_clients) * 100
        total_client_info = 'Stanowi to: {} / {} [{:.2f} %] wszystkich klientów'.format(total_clients_without_plt,
                                                                                        total_clients,
                                                                                        total_client_percent)
        logging.info(total_client_info)
        #  Sekcja odpowiedzialna za wyświetlania informacji o obciążeniach paczkomatów
        logging.info(' ')
        total_plt_load_average = np.sum(self.__plt_utilisation) / np.sum(self.__plt_map)
        logging.info('Średnie obciążenie paczkomatów wynosi: {} / {}'.format(total_plt_load_average, self.__p_max))
        total_plt_load_median = np.median(self.__plt_utilisation[self.__plt_map == 1])
        logging.info('Mediana obciążenia paczkomatów wynosi: {} / {}'.format(total_plt_load_median, self.__p_max))
        total_plt_load_max = np.max(self.__plt_utilisation)
        logging.info('Maksymalne obciążenie paczkomatów wynosi: {} / {}'.format(total_plt_load_max, self.__p_max))
        total_plt_load_min = np.min(self.__plt_utilisation[self.__plt_map == 1])
        logging.info('Minimalne obciążenie paczkomatów wynosi: {} / {}'.format(total_plt_load_min, self.__p_max))
        logging.info(' ')

    def plot_av_clients_at_given_range(self):
        fig, ax = plt.subplots(figsize=(16, 9))
        # Sortowanie według łacznego czasu wykonania
        # sorted_l = dict(sorted(self.__av_clients_at_given_range.items(), key=lambda x: x[1], reverse=True))
        sorted_l = self.__av_clients_at_given_range
        dist = sorted_l.keys()
        av_clients = sorted_l.values()
        # Generowanie wykresu
        y_pos = np.arange(len(dist))
        ax.barh(y_pos, av_clients, align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(dist)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('Średnia liczba klientów w danej komórce')
        ax.set_ylabel('Odległość do najbliższego paczkomatu')
        ax.set_title('Średnia ilość klientow w danej komórce w zależności od odległości do paczkomatu')
        save_plot_to_file(plt, 'srednia_ilosc_klientow_w_danej_odleglosc_od_paczkomatu')
        plt.show()

    def plot_av_dist_for_cell_with_given_cliens(self):
        fig, ax = plt.subplots(figsize=(16, 9))
        # Sortowanie według łacznego czasu wykonania
        # sorted_l = dict(sorted(self.__av_distance_for_clients_cell.items(), key=lambda x: x[1], reverse=True))
        sorted_l = self.__av_distance_for_clients_cell
        clients_no = sorted_l.keys()
        av_dist = sorted_l.values()
        # Generowanie wykresu
        y_pos = np.arange(len(clients_no))
        ax.barh(y_pos, av_dist, align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(clients_no)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('Średnia odległość do najbliższego paczkomatu')
        ax.set_ylabel('Ilość klientów w danej komórce')
        ax.set_title('Średnia odległość do najbliższego paczkomatu w zależności od ilości klientów w danej komórce')
        save_plot_to_file(plt, 'srednia_odleglosc_w_zal_od_ilosc_klientow')
        plt.show()

    def __calculate(self):
        """
            Funkcja wewnętrzna obliczająca macierze wykrozsytanie paczkomatów oraz stref ich działania
        """
        temp_client_map = np.copy(self.__client_map)
        self.__plt_utilisation_without_d_max = np.zeros(self.__map_shape)
        radius_of_plt = 0
        # Zakończ jak braknie klientów
        while (not np.all((self.__client_map == 0))) and (not np.all((self.__plt_map == 0))):
            for i in range(0, np.max(self.__client_map) + 1):
                for x_plt in range(0, self.__map_shape[0]):
                    for y_plt in range(0, self.__map_shape[1]):
                        if self.__plt_map[x_plt][y_plt] == 1:
                            self.__distribute_client_to_plt(x_plt, y_plt, radius_of_plt)

            radius_of_plt = radius_of_plt + 1
            if radius_of_plt > self.__map_shape[0] + self.__map_shape[1]:
                raise ValueError('Prosimy skontaktować sie z biurem obłsugi klienta :) ')
        self.__client_map = np.copy(temp_client_map)

        # trzeba zachować kolejność wywołań
        self.__calculate_distance_matrix()
        self.__calculate_av_clients()
        self.__calculate_av_distances()

    def __distribute_client_to_plt(self, x_plt: int, y_plt: int, radius: int):
        """
            Funckja przydzielające klientów do każdego paczkomatu
        """
        x_start = x_plt - radius
        if x_start < 0:
            x_start = 0
        x_end = x_plt + radius + 1
        if x_end > self.__map_shape[0]:
            x_end = self.__map_shape[0]
        for x in range(x_start, x_end):
            y_start = y_plt - radius
            if y_start < 0:
                y_start = 0
            y_end = y_plt + radius + 1
            if y_end > self.__map_shape[1]:
                y_end = self.__map_shape[1]
            for y in range(y_start, y_end):
                if np.abs(x_plt - x) + np.abs(y_plt - y) == radius:
                    if radius <= self.__d_max:
                        self.__client_within_plt_zone[x][y] = 1
                    if self.__client_map[x][y] > 0:
                        clients = 1
                        total_clients_per_plt = self.__plt_utilisation_without_d_max[x_plt][y_plt] + clients
                        self.__plt_utilisation_without_d_max[x_plt][y_plt] = total_clients_per_plt
                        self.__client_map[x][y] -= clients
                        if radius <= self.__d_max:  # Uwględnie zasiegu działania paczkomatu
                            self.__plt_utilisation[x_plt][y_plt] = total_clients_per_plt

    def __calculate_distance_matrix(self):
        """
        Funkcja obliczająca macierz self.__distance_matrix.
        :return:
        """
        diamond_list = [Helpers.diamond_edge(r) for r in range(self.__map_shape[0] + self.__map_shape[1])]
        for index, _ in np.ndenumerate(self.__distance_matrix):
            y, x = index
            for r in range(self.__map_shape[0] + self.__map_shape[1]):
                x_min = x - r if x - r > 0 else 0
                x_max = x + r + 1 if x + r + 1 < self.__map_shape[1] else self.__map_shape[1]
                y_min = y - r if y - r > 0 else 0
                y_max = y + r + 1 if y + r + 1 < self.__map_shape[0] else self.__map_shape[0]

                mx_min = r - (x - x_min)
                mx_max = r + (x_max - 1 - x) + 1
                my_min = r - (y - y_min)
                my_max = r + (y_max - 1 - y) + 1

                cut = self.__plt_map[y_min:y_max, x_min:x_max]
                mask = diamond_list[r][my_min:my_max, mx_min:mx_max]
                values = cut[mask]
                if np.any(values):
                    self.__distance_matrix[index] = r
                    break

    def __calculate_av_distances(self):
        """
        Funkcja licząca średnią odległość od paczkomatu dla komórek o zadanej ilości klientów.
        Modyfikuje self.__av_distance_for_clients_cell
        :return:
        """
        max_clients = int(np.max(self.__client_map))
        for clients_no in range(max_clients + 1):
            mask = self.__client_map == clients_no
            self.__av_distance_for_clients_cell[clients_no] = \
                np.sum(self.__distance_matrix[mask]) / np.count_nonzero(mask) if np.any(mask) else 0

    def __calculate_av_clients(self):
        """
        Funkcja licząca średnią ilość klientów w zadanej odległości od najbliższego paczkomatu.
        Modyfikuje self.__av_clients_at_given_range.
        :return:
        """
        max_dist = int(np.max(self.__distance_matrix))
        for dist in range(max_dist + 1):
            mask = self.__distance_matrix == dist
            self.__av_clients_at_given_range[dist] = \
                np.sum(self.__client_map[mask]) / np.count_nonzero(mask) if np.any(mask) else 0
