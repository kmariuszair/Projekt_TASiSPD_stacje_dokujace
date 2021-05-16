import sys
import json
import numpy as np
"""
    Klasa służąca do przechowywania ustawień wykonywania algorytmu oraz funkcji służących do łatwego zarządzania 
    ustawieniami. Każda funkcja korzystająca z zapisanych ustawień powinna mieć swoją własną funkcję do wczytywania
    danych. W celu zmiany ścieżki pliku ustawień należy użyć funkcji "change_path_to_settings_file".
    
    W celu wygenerowania domyślnych ustawień algorytmu, należy uruchomić ten plik.
"""


class SettingsMenager:
    def __init__(self, path='settings/settings.json'):
        self.default_path_to_settings = path

    def change_path_to_settings_file(self, new_path):
        """
        Zmień ścieżkę do pliku konfiguracyjnego
        :param new_path: Nowa ścieżka do pliku konfiguracyjnego
        :return:
        """
        self.default_path_to_settings = new_path

    def load_settings_from_file(self) -> dict:
        """
        Wczytaj plik konfiguracyjny
        :return: Zwróc słownik ze wszystkimi ustawieniami zawartymi w tym pliku
        """
        try:
            with open(self.default_path_to_settings, 'r') as json_file:
                data = json.load(json_file)
                json_file.close()
                return data
        except FileNotFoundError:
            with open('../' + self.default_path_to_settings, 'r') as json_file:
                data = json.load(json_file)
                json_file.close()
                return data

    def get_DataCollector_settings(self) -> dict:
        """
        Wczytaj ustawienia klasy DataCollector
        :return: Słownik z ustawieniami
        """
        data = self.load_settings_from_file()
        return data['DataCollectorPlotter'][0]

    def get_plot_client_map_settings(self) -> dict:
        """
        Wczytaj ustawienia funkcji plot_client_map (wcześniej: show_3D_client_map)
        :return: Słownik z ustawieniami
        """
        data = self.load_settings_from_file()
        if 'plot_client_map' in data.keys():  # Sprawdź czy plik konfiguracyjny używana nowego klucza
            return data['plot_client_map'][0]
        else:
            return data['show_3D_client_map'][0]

    def get_Solver_settings(self) -> dict:
        """
        Wczytaj ustawienia klasy Solver
        :return: Słownik z ustawieniami
        """
        data = self.load_settings_from_file()
        return data['main'][0]

    def get_PlotSaver_settings(self) -> dict:
        """
        Wczytaj ustawienia pliku PlotSaver
        :return: Słownik z ustawieniami
        """
        data = self.load_settings_from_file()
        return data['PlotSaver'][0]

    def get_RobotsSimulation_settings(self) -> dict:
        data = self.load_settings_from_file()
        return data['RobotsSimulation'][0]

    def get_client_map(self) -> np.array:
        """
        Wczytaj zdefiniowaną mapę klientów ze ścieżki zdefioniowanej w pliku konfiguracyjnym i zwróć tą macierz
        :return: Mapa rozmieszczenia klientów
        """
        data = self.get_Solver_settings()
        try:
            file = open(data['path_to_client_map'], 'rb')
            clients_map = np.load('..' + file)
            file.close()
        except:
            file = open(data['path_to_client_map'], 'rb')
            clients_map = np.load(file)
            file.close()
        return np.copy(clients_map)

    def save_settings_to_file(self, data: dict, path_to_save=None):
        """
        Zapis podanego pliku konfiguracyjnego na podanej ścieżce
        :param data: Sformatowany plik konfiguracyjny do zapisu
        :param path_to_save: Scieżka w której ma zostać zapisany plik
        :return:
        """
        if path_to_save is None:
            path_to_save = self.default_path_to_settings
        try:
            with open('../' + path_to_save, 'w') as json_file:
                json_file.write(json.dumps(data, indent=4))
                json_file.close()
                return data
        except FileNotFoundError:
            with open(path_to_save, 'w') as json_file:
                json_file.write(json.dumps(data, indent=4))
                json_file.close()
                return data
        except:
            raise ValueError('Error with save file')

    def generate_default_settings(self, path_to_save=None):
        """
        Generowanie pliku domyślnego z ustawieniami potrzebnymi do uruchomienia algorytmu,
        reprezentacji zebranych danych oraz zapisu uzyskanych wykresów do pliku.
        :param path_to_save: Ścieżka do folderu, gdzie ma zostać utworzony plik konfiguracyjny
        :return:
        """
        data = {}
        """
               Parametry odpowiedzielne za ustawienie warunków początkowych w main i klasie Solver 
        """
        data['main'] = []
        data['main'].append({
            'path_to_client_map': None,

            'map_shape': (20, 20),

            'clients_number': 500,
            'max_clients_number_in_cell': 10,

            'n_max': 20,
            'p_max': 30,
            'd_max': 3,
            'r': 1,
            "min_time_in_tl": 30,
            "min_time_in_lt_tl": 7,
            'time_lim': None,
            'iteration_lim': 5,

            'starting_solution': None
        })

        """
            Parametry odpowiedzialne za generowanie wykresów
        """
        data['DataCollectorPlotter'] = []
        data['DataCollectorPlotter'].append({
            'allow_generate_dynamic_map_animation': True,
            'connect_dots_on_plot': True,
            'show_plot_of_Q_a': True,
            'show_map_of_best_plt_position': True,
            'show_plot_of_total_taboo_list_elements': True,
            'show_map_of_total_moves': True,
            'show_plot_long_term_tabu_list_elements': True,
            'show_plot_elems_in_nei': True
        })

        """
            Parametry związane z generowaniem i wyświetlaniem mapy klientów
        """

        data['plot_client_map'] = []
        data['plot_client_map'].append({
            'generate_3D_rotate_GIF': False,
            'generate_2D': False,
            'save_to_gif': False
        })
        """
            Parametry potrzebne do zapisu wykresów do plików
        """
        data['PlotSaver'] = []
        data['PlotSaver'].append({
            'save_plot_to_file': False,
            'path_to_save_plot': None
        })
        self.save_settings_to_file(data, path_to_save)


"""
    Globalny byt klasy SettingsMenager w celu łatwiejszego zawiadywania ustawieniami.
    Jest on potrzebny do konfiguracji programu.
"""
setting_menager = SettingsMenager()


"""
    Uruchomienie tego pliku powoduje powstanie domyślnego pliku konfiguracyjnego w domyślnej scieżce programu
"""
if __name__ == '__main__':
    setting_menager.generate_default_settings()
    sys.exit(0)