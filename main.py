import numpy as np
import logging

import src.Solver
import src.ProblemGenerator
import src.SolutionGrader as SolutionGrader
import src.DataCollectorPlotter as DataCollectorPlotter
import src.SolutionUtilization as SolutionUtilization
from src.SettingMenager import setting_menager
import src.FileMenager as FileMenager
import src.MapGenerator as MapGenerator


def run_algorithm(path_to_settings=None):
    if path_to_settings is not None:
        setting_menager.change_path_to_settings_file(path_to_settings)

    data = setting_menager.get_Solver_settings()
    map_shape = data['map_shape']
    # clients_number = data['clients_number']
    # max_clients_number_in_cell = data['max_clients_number_in_cell']
    n_max = data['n_max']
    p_max = data['p_max']
    d_max = data['d_max']
    r = data['r']
    min_time_in_tl = data['min_time_in_tl']
    min_time_in_lt_tl = data['min_time_in_lt_tl']
    time_lim = data['time_lim']
    iteration_lim = data['iteration_lim']
    dynamic_neighborhood = data['dynamic_neighborhood']
    log_path = data['log_path']
    starting_solution = np.load(data['starting_solution']) if data['starting_solution'] else None

    log_file_path = log_path + '/' + path_to_settings.split('/')[-1][:-5] + '.log'
    if not FileMenager.is_path_to_file_exists(log_file_path):
        FileMenager.generate_path_to_file(log_file_path)
    open(log_file_path, 'w').close()  # czyści poprzednią wersję pliku z logiem
    # ustawienia loggera
    rootLogger = logging.getLogger()
    fileHandler = logging.FileHandler(log_file_path)
    rootLogger.addHandler(fileHandler)

    rootLogger.info('=========    Aktualny problem testowy: {}   ========='.format(path_to_settings.split('/')[-1][:-5]))

    robots_simulation_data = setting_menager.get_RobotsSimulation_settings()

    barriers_map = robots_simulation_data['barriers_map']
    docking_stations_map = robots_simulation_data['docking_stations_map']
    robots_number = robots_simulation_data['robots_number']
    sim_time = robots_simulation_data['sim_time']

    robots_simulation = MapGenerator.TrafficMapGenerator(barriers_map, docking_stations_map, robots_number)

    traffic_map = robots_simulation.generate_map(sim_time)

    DataCollectorPlotter.plot_client_map(traffic_map, np.max(traffic_map) + 1)
    logging.info("Inicjalizuję solwer")
    solver = src.Solver.Solver(n_max,
                               p_max,
                               d_max,
                               r,
                               min_time_in_tl,
                               min_time_in_lt_tl,
                               traffic_map,
                               iteration_lim=iteration_lim,
                               dynamic_neighborhood=dynamic_neighborhood,
                               starting_solution=docking_stations_map)
    # ustawiamy limit iteracji, ewenetualnie można ustawić limit czasu, nie dajemy własnego rozwiązania początkowego
    # tylko pozwalamy generatorowi wygenerować to rozwiązanie
    logging.info("Rozpoczynam rozwiązywanie problemu")
    solution = solver.solve(record_and_plot_data=True, telemetry_on=True)
    # Sprawdzanie wariancji uzyskanych wyników
    solution_grader = SolutionGrader.SolutionGrader(traffic_map, solution)
    solution_res = solution_grader.grade_solution(traffic_map, solution)
    # Wyznacz mapę wykorzystania stacji dokujących
    solution_util = SolutionUtilization.SolutionUtilization(traffic_map, solution, p_max, d_max)
    # Pokaż i zapis do pliku wykresy uzyskanego rozwiązania
    solution_util.plot_solution_utilization()
    solution_util.plot_clients_within_plt_zone()
    solution_util.plot_solution_utilization_without_d_max()
    solution_util.plot_av_clients_at_given_range()
    solution_util.plot_av_dist_for_cell_with_given_cliens()
    # Pokaż w konsoli informacje o uzyskanym rozwiązaniu
    solution_util.print_solution_utilization_data()

    # zamknij plik z logami
    rootLogger.removeHandler(fileHandler)


if __name__ == "__main__":
    list_of_settings = [
        # 'settings/test_cases/case1.json'
    ]

    itr_count = 1

    rootLogger = logging.getLogger()

    consoleHandler = logging.StreamHandler()
    rootLogger.addHandler(consoleHandler)
    rootLogger.level = logging.INFO

    for path in list_of_settings:
        itr_count += 1
        run_algorithm(path)
    rootLogger.info('=================================')
    rootLogger.info('Generowanie rozwiązań zakończone!')
