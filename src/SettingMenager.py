import sys
import json
import numpy as np


class SettingsMenager:
    def __init__(self, path='settings/settings.json'):
        self.default_path_to_settings = path

    def change_path_to_settings_file(self, new_path):

        self.default_path_to_settings = new_path
        self.plot_data = self.load_settings_from_file()

    def load_settings_from_file(self) -> dict:

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

        data = self.load_settings_from_file()
        return data['DataCollectorPlotter'][0]

    def get_plot_client_map_settings(self) -> dict:

        data = self.load_settings_from_file()
        if 'plot_client_map' in data.keys():
            return data['plot_client_map'][0]
        else:
            return data['show_3D_client_map'][0]

    def get_Solver_settings(self) -> dict:

        data = self.load_settings_from_file()
        return data['main'][0]

    def get_PlotSaver_settings(self) -> dict:

        return self.plot_data['PlotSaver'][0]

    def get_RobotsSimulation_settings(self) -> dict:
        data = self.load_settings_from_file()
        return data['RobotsSimulation'][0]

    def get_client_map(self) -> np.array:

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

        data = {}

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

        data['plot_client_map'] = []
        data['plot_client_map'].append({
            'generate_3D_rotate_GIF': False,
            'generate_2D': False,
            'save_to_gif': False
        })

        data['PlotSaver'] = []
        data['PlotSaver'].append({
            'save_plot_to_file': False,
            'path_to_save_plot': None
        })
        self.save_settings_to_file(data, path_to_save)



setting_menager = SettingsMenager()


if __name__ == '__main__':
    setting_menager.generate_default_settings()
    sys.exit(0)