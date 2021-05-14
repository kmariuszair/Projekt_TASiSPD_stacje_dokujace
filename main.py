import numpy as np
import logging

import src.Solver
import src.ProblemGenerator
import src.SolutionGrader as SolutionGrader
import src.DataCollectorPlotter as DataCollectorPlotter
import src.SolutionUtilization as SolutionUtilization
from src.SettingMenager import setting_menager
import src.FileMenager as FileMenager


def run_algorithm(path_to_settings=None):
    if path_to_settings is not None:
        setting_menager.change_path_to_settings_file(path_to_settings)

    data = setting_menager.get_Solver_settings()
    map_shape = data['map_shape']
    clients_number = data['clients_number']
    max_clients_number_in_cell = data['max_clients_number_in_cell']
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

    # Wczytaj zdefiniowaną macierz klientów lub wygeneruj losową
    clients_map = None
    p_gen = src.ProblemGenerator.RandomProblemGen(map_shape, clients_number, max_clients_number_in_cell)
    if data['path_to_client_map'] is None:
        clients_map = p_gen.generate_problem()
        logging.info("Generuję losowy problem do rozwiązania")
    else:
        clients_map = setting_menager.get_client_map()
        logging.info("Wczytuje problem do rozwiązania z pliku")

    DataCollectorPlotter.plot_client_map(clients_map, max_clients_number_in_cell)
    logging.info("Inicjalizuję solwer")
    solver = src.Solver.Solver(n_max,
                               p_max,
                               d_max,
                               r,
                               min_time_in_tl,
                               min_time_in_lt_tl,
                               clients_map,
                               iteration_lim=iteration_lim,
                               dynamic_neighborhood=dynamic_neighborhood,
                               starting_solution=starting_solution)
    # ustawiamy limit iteracji, ewenetualnie można ustawić limit czasu, nie dajemy własnego rozwiązania początkowego
    # tylko pozwalamy generatorowi wygenerować to rozwiązanie
    logging.info("Rozpoczynam rozwiązywanie problemu")
    solution = solver.solve(record_and_plot_data=True, telemetry_on=True)
    # Sprawdzanie wariancji uzyskanych wyników
    solution_grader = SolutionGrader.SolutionGrader(clients_map, solution)
    solution_res = solution_grader.grade_solution(clients_map, solution)
    # Wyznacz mapę wykorzystania paczkomatów
    solution_util = SolutionUtilization.SolutionUtilization(clients_map, solution, p_max, d_max)
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
    # OK - oznacza, że ograniczenia działają
    list_of_settings = [
        # długo sie liczy
        # 'settings/test_cases/case1/1a.json', # OK
        # 'settings/test_cases/case1/1b.json', # OK
        # 'settings/test_cases/case1/1c.json', # OK
        # 'settings/test_cases/case1/1d.json', # OK
        # 'settings/test_cases/case1/1e.json',

        # 'settings/test_cases/case2/2a.json', # OK
        # 'settings/test_cases/case2/2b.json', # OK
        # 'settings/test_cases/case2/2c.json', # OK

        # 'settings/test_cases/case3/3a.json', # OK
        # 'settings/test_cases/case3/3b.json', # OK
        # 'settings/test_cases/case3/3c.json',

        # 'settings/test_cases/case4/4a.json', # OK
        # 'settings/test_cases/case4/4b.json', # OK
        # 'settings/test_cases/case4/4c.json', # OK
        # 'settings/test_cases/case4/4d.json', # OK

        # 'settings/test_cases/case5/5a.json', # OK
        # 'settings/test_cases/case5/5b.json', # OK
        # 'settings/test_cases/case5/5c.json', # OK

        # 'settings/test_cases/case6/6a.json', # OK
        # 'settings/test_cases/case6/6b.json', # OK
        # 'settings/test_cases/case6/6c.json', # OK

        # 'settings/test_cases/case7/7a.json', # OK
        # 'settings/test_cases/case7/7b.json', # OK
        # 'settings/test_cases/case7/7c.json', # OK

        # 'settings/test_cases/case8/8a.json', # OK
        # 'settings/test_cases/case8/8b.json', # OK
        # 'settings/test_cases/case8/8c.json', # OK

        # 'settings/test_cases/case9/9a.json', # OK
        # 'settings/test_cases/case9/9b.json', # OK
        # 'settings/test_cases/case9/9c.json', # OK

        # bardzo długo się liczy
        # 'settings/test_cases/case10/10real.json',
        # 'settings/test_cases/case10/10random.json',

        # bardzo długo się liczy
        # 'settings/test_cases/case10/10breal.json', # OK
        # 'settings/test_cases/case10/10brandom.json',

        # 'settings/test_cases/case11/11comp_surv.json',
        # 'settings/test_cases/case11/11tabu.json',

        # 'settings/test_cases/case11/11bcomp_surv.json',
        # 'settings/test_cases/case11/11btabu.json'

        # 'settings/test_cases/case12/12_static.json', # OK
        # 'settings/test_cases/case12/12_dynamic.json', # OK

        # 'settings/test_cases/case12/12b_static.json', # OK
        # 'settings/test_cases/case12/12b_dynamic.json' # OK

        # 'settings/test_cases/case13/13_1.json',  # OK
        # 'settings/test_cases/case13/13_2.json',  # OK
        # 'settings/test_cases/case13/13_3.json',  # OK
        # 'settings/test_cases/case13/13_4.json',  # OK
        # 'settings/test_cases/case13/13_5.json',  # OK
        # 'settings/test_cases/case13/13_6.json',  # OK
        # 'settings/test_cases/case13/13_7.json',  # OK
        # 'settings/test_cases/case13/13_8.json',  # OK
        # 'settings/test_cases/case13/13_9.json',  # OK
        # 'settings/test_cases/case13/13_10.json'  # OK

        'settings/test_cases/case14/14_even.json',  # OK
        'settings/test_cases/case14/14_peak.json'  # OK
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
