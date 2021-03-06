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
import src.Helpers as Helpers
import cv2
import pickle


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

    robots_simulation_data = setting_menager.get_RobotsSimulation_settings()
    docks_no = robots_simulation_data['docking_stations_no']

    org_dir = setting_menager.plot_data['PlotSaver'][0]['path_to_save_plot']

    robots_details_path = robots_simulation_data["robots_settings"]
    robots_settings = None
    if robots_details_path is not None:
        with open(robots_details_path, 'rb') as robots_details_f:
            robots_details = pickle.load(robots_details_f)
            robots_details_f.close()

        robots_settings = []
        for _, robot_detail in robots_details.items():
            robots_settings.append(Helpers.make_robot_setting_from_dict(robot_detail))

    docking_stations_details_path = robots_simulation_data["docks_settings"]
    docking_stations_details = None
    if docking_stations_details_path is not None:
        with open(docking_stations_details_path, 'rb') as docking_stations_details_f:
            docking_stations_details = pickle.load(docking_stations_details_f)
            docking_stations_details_f.close()

    for docks_number in range(max(docks_no//2, 1), max(docks_no, 2), max((docks_no - docks_no//2)//5, 1)):

        setting_menager.plot_data['PlotSaver'][0]['path_to_save_plot'] = org_dir + '/docks_no_{}'.format(docks_number)

        log_file_path = log_path + '/' + path_to_settings.split('/')[-1][:-5] + '_{}_docks'.format(docks_number) + '.log'
        if not FileMenager.is_path_to_file_exists(log_file_path):
            FileMenager.generate_path_to_file(log_file_path)
        open(log_file_path, 'w').close()  # czy??ci poprzedni?? wersj?? pliku z logiem
        # ustawienia loggera
        rootLogger = logging.getLogger()
        fileHandler = logging.FileHandler(log_file_path)
        rootLogger.addHandler(fileHandler)

        rootLogger.info('=========    Aktualny problem testowy: {}   ========='.format(path_to_settings.split('/')[-1][:-5]))

        rootLogger.info('Liczba stacji dokuj??cych: ' + str(docks_number))

        barriers_map = np.load(robots_simulation_data['barriers_map']) if robots_simulation_data['barriers_map'] else None
        # Dylatacja na map?? barier w celu omini??cia i nie blokowania p??l truskawek
        #TODO: Wybierz jeden z poni??szych tryb??w; doda?? do listy konfiguracyjnej
        barriers_map_w_d = cv2.dilate(barriers_map.astype(np.uint8), np.ones((3,3),np.uint8))
        # barriers_map_w_d = barriers_map
        # ZMIANA STRATEGII - zamiast zadawa?? pocz??tkow?? map?? stacji, to j?? losujemy
        docks_no = robots_simulation_data['docking_stations_no']
        frame = robots_simulation_data['frame']
        max_investment_cost = robots_simulation_data['max_investment_cost']
        max_maintenance_cost = robots_simulation_data['max_maintenance_cost']
        rootLogger.info("Generuj?? pocz??tkowe pozycje stacji dokuj??cych")
        if docking_stations_details is not None:
            rootLogger.info("U??ywam informacji o stacjach wczytanych z pliku")
        i = 0
        investment_cost, maintenance_costs = np.inf, np.inf
        while investment_cost > max_investment_cost and maintenance_costs > max_maintenance_cost and i < 10000:
            docking_stations_map, investment_cost, maintenance_costs = Helpers.generate_docking_stations_map(barriers_map_w_d, docks_number, frame, docks_params=docking_stations_details)
            i += 1
        if investment_cost > max_investment_cost or maintenance_costs > max_maintenance_cost:
            rootLogger.info('Nie mo??na wygenerowa?? pocz??tkowego uk??adu stacji dokuj??cych' +
                            ' o koszczcie mniejszym od maksymalnego.' +
                            ' Koszt: %.2f' % investment_cost + ', koszt utrzymania: %.2f' % maintenance_costs)
        else:
            rootLogger.info("Koszt wygenerowanego przypadku testowego: %.2f" % investment_cost)
            rootLogger.info("Koszt utrzymania wygenerowanego przypadku: %.2f" % maintenance_costs)
            # docking_stations_map = np.load(robots_simulation_data['docking_stations_map']) if robots_simulation_data['docking_stations_map'] else None
            robots_number = robots_simulation_data['robots_number']
            sim_time = robots_simulation_data['sim_time']

            if robots_settings is not None:
                rootLogger.info("U??ywam informacji o robotach wczytanych z pliku")
            robots_simulation = MapGenerator.TrafficMapGenerator(barriers_map, docking_stations_map, robots_number, robots_swarm_predefined_settings=robots_settings)

            traffic_map, _, _, robot_pos_sim, cumulative_gain, cumulative_loading_times, cumulative_awaiting_times, \
            cum_dist_to_dock_when_bat_low, no_trips_to_docking_stations = robots_simulation.generate_map(sim_time)

            rootLogger.info("????czny zysk z inwestycji: " + str(cumulative_gain))
            rootLogger.info("????czny czas ??adowania: " + str(cumulative_loading_times))
            rootLogger.info("????czny czas oczekiwania na ??adowanie: " + str(cumulative_awaiting_times))
            rootLogger.info("????czna odleg??o???? do stacji ??aduj??cej, gdy roboty przechodz?? w stan niskiej baterii: " + str(cum_dist_to_dock_when_bat_low))
            rootLogger.info("????czna ilo???? przejazd??w do stacji dokuj??cych: " + str(int(no_trips_to_docking_stations)))

            # Wizualizacja mapy rozmieszczenia barrier oraz trajektorii ruchu robot??w
            DataCollectorPlotter.plot_map_barriers(barriers_map)
            rootLogger.info("Rysuj?? szkic ruch??w robot??w")
            DataCollectorPlotter.plot_robots_movements(robot_pos_sim, barriers_map)
            rootLogger.info("Tworz?? animacj?? ruchu robot??w")
            DataCollectorPlotter.robot_anim_2.robot_animation(robot_pos_sim, barriers_map)

            rootLogger.info("Rysuj?? wykres obci????enia mapy ruchem robot??w")
            DataCollectorPlotter.plot_client_map(traffic_map.astype('int32'), int(np.max(traffic_map) + 1))

            logging.info("Inicjalizuj?? solwer")
            docking_stations_map = (docking_stations_map > 0).astype('int32')
            solver = src.Solver.Solver(np.sum((docking_stations_map > 0).astype('int32')),
                                       p_max,
                                       d_max,
                                       r,
                                       min_time_in_tl,
                                       min_time_in_lt_tl,
                                       traffic_map,
                                       frame,
                                       iteration_lim=iteration_lim,
                                       dynamic_neighborhood=dynamic_neighborhood,
                                       starting_solution=docking_stations_map,
                                       banned_positions=barriers_map_w_d)
            # ustawiamy limit iteracji, ewentualnie mo??na ustawi?? limit czasu
            logging.info("Rozpoczynam rozwi??zywanie problemu")
            solution = solver.solve(record_and_plot_data=True, telemetry_on=True)
            # Sprawdzanie wariancji uzyskanych wynik??w
            solution_grader = SolutionGrader.SolutionGrader(traffic_map, solution)
            solution_res = solution_grader.grade_solution(traffic_map, solution)
            # Wyznacz map?? wykorzystania stacji dokuj??cych
            solution_util = SolutionUtilization.SolutionUtilization(traffic_map.astype('int32'), solution.astype('int32'), p_max, d_max)
            # Wyznacz mape przemieszczen symulacyjnych robotow z optymalna pozycja stacji dokujacych
            DataCollectorPlotter.plot_robots_movements_with_doc_station(robot_pos_sim, barriers_map, solution)
            rootLogger.info("Tworz?? animacj?? optymalizacji pozycji stacji dokuj??cych")
            DataCollectorPlotter.robot_anim_2.robot_animation_with_doc_station(robot_pos_sim, barriers_map, solution)

            # Poka?? i zapis do pliku wykresy uzyskanego rozwi??zania
            solution_util.plot_solution_utilization()
            solution_util.plot_clients_within_plt_zone()
            solution_util.plot_solution_utilization_without_d_max()
            solution_util.plot_av_clients_at_given_range()
            solution_util.plot_av_dist_for_cell_with_given_cliens()
            # Poka?? w konsoli informacje o uzyskanym rozwi??zaniu
            solution_util.print_solution_utilization_data()
        # zamknij plik z logami
        rootLogger.removeHandler(fileHandler)


if __name__ == "__main__":
    list_of_settings = [
        'settings/test_cases/case1.json',  # Przypadek testowy case 1
        'settings/test_cases/case2.json',
        'settings/test_cases/case3.json'  # Najlepsza (chyba) szklarnia
        # 'settings/test_cases/case4.json',  # Najbardziej realna szklarnia
        # 'settings/test_cases/case5.json'    # Przypadek case5 z??o??liwy - 1 stacja dokuj??ca
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
    rootLogger.info('Generowanie rozwi??za?? zako??czone!')
