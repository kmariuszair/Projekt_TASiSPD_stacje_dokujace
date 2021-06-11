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
import cv2

def run_algorithm(path_to_settings=None):
    if path_to_settings is not None:
        setting_menager.change_path_to_settings_file(path_to_settings)

    data = setting_menager.get_Solver_settings()
    n_max = data['n_max']
    p_max = data['p_max']
    d_max = data['d_max']
    r = data['r']
    min_time_in_tl = data['min_time_in_tl']
    min_time_in_lt_tl = data['min_time_in_lt_tl']
    iteration_lim = data['iteration_lim']
    dynamic_neighborhood = data['dynamic_neighborhood']
    log_path = data['log_path']

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

    barriers_map = np.load(robots_simulation_data['barriers_map']) if robots_simulation_data['barriers_map'] else None
    docking_stations_map = np.load(robots_simulation_data['docking_stations_map']) if robots_simulation_data['docking_stations_map'] else None
    robots_number = robots_simulation_data['robots_number']
    sim_time = robots_simulation_data['sim_time']

    robots_simulation = MapGenerator.TrafficMapGenerator(barriers_map, docking_stations_map, robots_number)

    traffic_map, _, _, robot_pos_sim, _, _, _, _, _ = robots_simulation.generate_map(sim_time)

    # Wizualizacja mapy rozmieszczenia barrier oraz trajektorii ruchu robotów
    DataCollectorPlotter.plot_map_barriers(barriers_map)
    DataCollectorPlotter.plot_robots_movements(robot_pos_sim, barriers_map)
    DataCollectorPlotter.dinozaur_pimpus.robot_animation(robot_pos_sim, barriers_map)

    DataCollectorPlotter.plot_client_map(traffic_map.astype('int32'), int(np.max(traffic_map) + 1))
    # Dylatacja na mapę barier w celu ominięcia i nie blokowania pól truskawek
    #TODO: Wybierz jeden z poniższych trybów; dodać do listy konfiguracyjnej
    barriers_map_w_d = cv2.dilate(barriers_map.astype(np.uint8), np.ones((3,3),np.uint8))
    # barriers_map_w_d = barriers_map

    logging.info("Inicjalizuję solwer")
    docking_stations_map = (docking_stations_map > 0).astype('int32')
    solver = src.Solver.Solver(np.sum((docking_stations_map > 0).astype('int32')),
                               p_max,
                               d_max,
                               r,
                               min_time_in_tl,
                               min_time_in_lt_tl,
                               traffic_map,
                               iteration_lim=iteration_lim,
                               dynamic_neighborhood=dynamic_neighborhood,
                               starting_solution=docking_stations_map,
                               banned_positions=barriers_map_w_d)
    # ustawiamy limit iteracji, ewentualnie można ustawić limit czasu
    logging.info("Rozpoczynam rozwiązywanie problemu")
    solution = solver.solve(record_and_plot_data=True, telemetry_on=True)
    # Sprawdzanie wariancji uzyskanych wyników
    solution_grader = SolutionGrader.SolutionGrader(traffic_map, solution)
    solution_res = solution_grader.grade_solution(traffic_map, solution)
    # Wyznacz mapę wykorzystania stacji dokujących
    solution_util = SolutionUtilization.SolutionUtilization(traffic_map.astype('int32'), solution.astype('int32'), p_max, d_max)
    # Wyznacz mape przemieszczen symulacyjnych robotow z optymalna pozycja stacji dokujacych
    DataCollectorPlotter.plot_robots_movements_with_doc_station(robot_pos_sim, barriers_map, solution)
    DataCollectorPlotter.dinozaur_pimpus.robot_animation_with_doc_station(robot_pos_sim, barriers_map, solution)

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
        # 'settings/test_cases/case1.json'  # Przypadek testowy case 1
        # 'settings/test_cases/case3.json'  # Najlepsza (chyba) szklarnia
        # 'settings/test_cases/case4.json'  # Najbardziej realna szklarnia
        'settings/test_cases/case5.json'    # Przypadek case4 złośliwy - 1 stacja dokująca
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
