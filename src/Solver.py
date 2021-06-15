import numpy as np
from typing import Tuple, Callable
import time
from functools import wraps, partial
import inspect
import logging

import src.ConditionTester as ConditionTester
import src.StartingSolutionGenerator as StartingSolutionGenerator
import src.NeighborhoodGenerator as NeighborhoodGenerator
import src.DataCollectorPlotter as DataCollectorPlotter
import src.Helpers as Helpers


class Telemetry:

    telemetry_data = {}

    telemetry_on = True

    @staticmethod
    def print_telemetry():

        logging.info("{:>40}".format("TELEMETRIA"))

        logging.info("{:<50} {:>15}".format('NAZWA METODY', 'CZAS [S]'))


        for key, value in zip(Telemetry.telemetry_data.keys(), Telemetry.telemetry_data.items()):
            name, comp_time = value
            logging.info("{:<50} {:>10}.{}".format(name, int(np.floor(comp_time)), int((comp_time % 1)*100)))

    @staticmethod
    def get_telemetry_data():
        return dict.copy(Telemetry.telemetry_data)

    @staticmethod
    def telemetry(method: Callable = None, class_name: str = 'Solver'):

        if method is None:
            return partial(Telemetry.telemetry)

        method_name = method.__name__

        if method_name[0:2] == '__' and not method_name[-2:] == '__':
            method_name = '_' + class_name + method_name

        @wraps(method)
        def time_telemetry_wrapper(*args, **kwargs):
            if Telemetry.telemetry_on:
                start = time.time()
                to_return = method(*args, **kwargs)
                stop = time.time()
                diff = stop - start
                Telemetry.telemetry_data[method_name] += diff
            else:
                to_return = method(*args, **kwargs)
            return to_return

        return time_telemetry_wrapper



def for_all_methods_and_class(decorator_cls, decorator_fun):
    def decorate(cls, *args, **kwargs):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)) and not attr == "__init__":
                setattr(cls, attr, decorator_fun(getattr(cls, attr), *args, **kwargs))
        for attr in decorator_cls.__dict__:
            if not callable(getattr(decorator_cls, attr)):
                if attr[0:2] == '__' and not attr[-2:] == '__':
                    setattr(cls, attr, getattr(decorator_cls, attr))
        return cls
    return decorate


@for_all_methods_and_class(Telemetry, Telemetry.telemetry)
class Solver:

    def __init__(self,
                 n_max: int,
                 p_max: int,
                 d_max: int,
                 r: int,
                 min_time_in_tl: int,
                 min_time_in_lt_tl: int,
                 client_map: np.array,
                 frame: int = 1,

                 record_and_plot_data: bool = False,

                 time_lim: float = None,
                 iteration_lim: int = None,

                 dynamic_neighborhood: bool = True,

                 telemetry_on: bool = False,

                 starting_solution: np.array = None,
                 banned_positions: np.array = None):

        self.__n_max = n_max
        self.__p_max = p_max
        self.__d_max = d_max

        self.__r = r
        self.__min_time_in_tl = min_time_in_tl
        self.__min_time_in_lt_tl = min_time_in_lt_tl
        self.__client_map = np.copy(client_map)
        self.__banned_positions = banned_positions

        self.__condition_tester = ConditionTester.OneConditionTester(p_max=self.__p_max,
                                                                     d_max=self.__d_max,
                                                                     clients_map=self.__client_map,
                                                                     banned_positions=self.__banned_positions,
                                                                     frame=frame)

        self.__record_and_plot_data = record_and_plot_data

        self.__dynamic_neighborhood = dynamic_neighborhood


        self.__collect_and_represent_data = DataCollectorPlotter.DataCollectorPlotter(client_map, load_setting_from_file=True)

        self.__time_lim = time_lim
        self.__iteration_lim = iteration_lim
        if self.__time_lim is None and self.__iteration_lim is None:
            raise ValueError("Nie podano warunku stopu dla algorytmu! Podaj maksymalną ilość iteracji lub czas obliczeń")
        if not (self.__time_lim is None) and not (self.__iteration_lim is None):
            raise ValueError("Podano dwa kryteria stopu, podaj tylko jeden")

        self.__clients_number = np.sum(self.__client_map)

        self.__map_shape = client_map.shape

        self.__tabu_list = np.zeros(self.__map_shape, dtype='int32')
        self.__long_term_tabu_list = np.zeros(self.__map_shape, dtype='int32')

        self.__default_starting_sol_gen = StartingSolutionGenerator.StartingSolutionGen(self.__n_max,
                                                                                        self.__p_max,
                                                                                        self.__d_max,
                                                                                        self.__client_map)

        self.__diamond_list = [Helpers.diamond_edge(r) for r in range(self.__map_shape[0] + self.__map_shape[1])]

        Telemetry.telemetry_on = telemetry_on
        Telemetry.telemetry_data = {**Telemetry.telemetry_data,
                                    **{method_name: 0 for method_name, method in
                                       inspect.getmembers(Solver, predicate=inspect.isfunction)}}

        if not (starting_solution is None):
            if np.sum((starting_solution > 0).astype('int32')) == self.__n_max and self.__is_solution_allowed(starting_solution):
                self.__starting_solution = np.copy(starting_solution)
            else:
                if self.__record_and_plot_data:
                    logging.info("Przekazane rozwiązanie początkowe nie spełnia kryteriów. Użyty zostanie domyślny generator")
                self.__starting_solution = None
        else:
            self.__starting_solution = None


        self.__curr_time = 0
        self.__curr_it = 0

        self.__x_a = None
        self.__Q_a = np.inf
        self.__x_min = None
        self.__Q_min = np.inf
        self.__x_min_new = None
        self.__Q_min_new = np.inf
        self.__x_min_new_tabu = None
        self.__Q_min_new_tabu = np.inf

    def solve(self, record_and_plot_data: bool = False, telemetry_on: bool = False) -> np.array:
        self.__record_and_plot_data = record_and_plot_data
        Telemetry.telemetry_on = telemetry_on
        to_return = self.__solve()
        logging.info("Najlepsze rozwiązanie ma koszt: %.2f" % self.__Q_min)

        if record_and_plot_data:
            Telemetry.print_telemetry()

            DataCollectorPlotter.generate_plot_of_telemetry(Telemetry.get_telemetry_data())

        self.__collect_and_represent_data.plot_data()
        return to_return

    def __solve(self) -> np.array:

        start_time = time.time()
        self.__curr_time = 0
        self.__curr_it = 0

        if self.__record_and_plot_data:
            logging.info("Generuję rozwiązanie początkowe")
        self.__x_a = self.__get_starting_solution()
        self.__x_min = np.copy(self.__x_a)
        self.__Q_a = self.__cost(self.__x_a)
        self.__Q_min = self.__Q_a

        logging.info("Koszt rozwiązania początkowego: %.2f" % self.__Q_a)
        self.__collect_and_represent_data.collect_data(self.__x_a, self.__Q_a, self.__tabu_list,
                                                       self.__long_term_tabu_list, 0,
                                                       0, 0,
                                                       0, 0)

        while not self.__stop_condition():

            self.__curr_it += 1
            if self.__record_and_plot_data:
                logging.info("Iteracja: " + str(self.__curr_it))
                logging.info("Aktualne rozwiązanie ma koszt: %.2f" % self.__Q_a)

            self.__Q_min_new = np.inf
            self.__Q_min_new_tabu = np.inf
            self.__x_min_new = None
            self.__x_min_new_tabu = None

            elems_in_nei = 0
            elems_in_short_tabu = 0
            elems_in_long_tabu = 0
            av_cadence = 0
            av_long_cadence = 0

            if self.__record_and_plot_data:
                logging.info("Przeszukuję sąsiedztwo")

            for neighbor in self.__yield_neighbor():
                elems_in_nei += 1
                if self.__is_solution_allowed(neighbor):
                    x_new = neighbor
                    Q_new = self.__cost(x_new)
                    is_in_long_tabu, long_cadence = self.__is_in_long_term_tabu_list(x_new)
                    if not is_in_long_tabu:
                        is_in_tabu, cadence = self.__is_in_tabu_list(x_new)
                        if not is_in_tabu:
                            if Q_new < self.__Q_min_new:
                                self.__Q_min_new = Q_new
                                self.__x_min_new = np.copy(x_new)
                        else:


                            av_cadence += cadence
                            elems_in_short_tabu += 1
                            if Q_new < self.__Q_min_new_tabu:
                                self.__Q_min_new_tabu = Q_new
                                self.__x_min_new_tabu = np.copy(x_new)
                    else:


                        av_long_cadence += long_cadence
                        elems_in_long_tabu += 1
                        if Q_new < self.__Q_min_new_tabu:
                            self.__Q_min_new_tabu = Q_new
                            self.__x_min_new_tabu = np.copy(x_new)
                if (self.__Q_min_new < 0.5 * (self.__Q_min + self.__Q_a)) and self.__dynamic_neighborhood:
                    break

            logging.info('Przeszukano ' + str(elems_in_nei) + ' elementów z sąsiedztwa')


            av_cadence = float(av_cadence / elems_in_short_tabu if elems_in_short_tabu > 0 else self.__min_time_in_tl)
            av_long_cadence = float(av_long_cadence / elems_in_long_tabu if elems_in_long_tabu > 0 else
                                    self.__min_time_in_lt_tl)

            av_cadence = self.__min_time_in_tl - av_cadence
            av_long_cadence = self.__min_time_in_lt_tl - av_long_cadence

            prev_x_a = np.copy(self.__x_a)
            self.__x_a = np.copy(self.__x_min_new) if not (self.__x_min_new is None) else None
            self.__Q_a = self.__Q_min_new

            if self.__aspiration_criteria():
                self.__x_a = np.copy(self.__x_min_new_tabu)
                self.__Q_a = self.__Q_min_new_tabu

                if self.__is_in_long_term_tabu_list(self.__x_a)[0]:

                    move = prev_x_a - self.__x_a
                    self.__delete_given_move_from_long_term_tabu(move == 1)


                    if self.__is_in_tabu_list(self.__x_a)[0]:
                        move = (self.__tabu_list > 0) * (self.__x_a > 0)
                        self.__delete_given_move_from_tabu(move)
                else:

                    move = (self.__tabu_list > 0) * (self.__x_a > 0)
                    self.__delete_given_move_from_tabu(move)
            if self.__Q_a < self.__Q_min:


                self.__x_min = np.copy(self.__x_a)
                self.__Q_min = self.__Q_a
            if self.__x_a is None:
                if self.__record_and_plot_data:
                    logging.info("Nie znaleziono nowego rozwiązania w sąsiedztwie")
                break



            self.__change_times_to_left_tl()
            self.__change_times_to_left_lt_tl()
            move = prev_x_a - self.__x_a
            self.__add_move_to_tabu_list(move)
            self.__add_move_to_long_term_tabu_list(move)


            self.__curr_time = time.time() - start_time


            self.__collect_and_represent_data.collect_data(self.__x_a, self.__Q_a, self.__tabu_list,
                                                           self.__long_term_tabu_list, elems_in_nei,
                                                           av_cadence, av_long_cadence,
                                                           elems_in_short_tabu, elems_in_long_tabu)
        return self.__x_min

    def __yield_neighbor(self):
        return NeighborhoodGenerator.neighborhood_generator(self.__x_a, self.__r)

    def __get_starting_solution(self):

        if not (self.__starting_solution is None):
            if self.__record_and_plot_data:
                logging.info("Używam zadanego rozwiązania początkowego")
            return self.__starting_solution
        else:
            if self.__record_and_plot_data:
                logging.info("Generuję automatycznie możliwie najlepsze rozwiązanie początkowe")
            return self.__default_starting_sol_gen.generate()

    def __cost(self, x_new: np.array) -> int:

        cost = 0
        for index, value in np.ndenumerate(self.__client_map):
            if value > 0:
                cost += value * self.__dist_to_nearest_pl(index, x_new)

        return cost

    def __dist_to_nearest_pl(self, actual_point: Tuple[int, int], pl_map: np.array) -> int:

        y, x = actual_point
        if pl_map[y, x]:
            return 0
        for r in range(self.__map_shape[0] + self.__map_shape[1]):
            x_min = x - r if x - r > 0 else 0
            x_max = x + r + 1 if x + r + 1 < self.__map_shape[1] else self.__map_shape[1]
            y_min = y - r if y - r > 0 else 0
            y_max = y + r + 1 if y + r + 1 < self.__map_shape[0] else self.__map_shape[0]

            mx_min = r - (x - x_min)
            mx_max = r + (x_max - 1 - x) + 1
            my_min = r - (y - y_min)
            my_max = r + (y_max - 1 - y) + 1

            cut = pl_map[y_min:y_max, x_min:x_max]
            mask = self.__diamond_list[r][my_min:my_max, mx_min:mx_max]
            values = cut[mask]
            if np.any(values):
                return r if r <= self.__d_max else self.__d_max*(2 - np.exp(-(r - self.__d_max)/self.__d_max))

    def __is_in_tabu_list(self, x_new: np.array) -> Tuple[bool, float]:

        diff = x_new - self.__tabu_list
        pl_not_in_forbidden_places = np.count_nonzero(diff > 0)

        is_in_tabu = pl_not_in_forbidden_places < self.__n_max
        cadence = self.__tabu_list[(diff <= 0) * (x_new > 0)] if is_in_tabu else 0

        return is_in_tabu, float(cadence)

    def __is_in_long_term_tabu_list(self, x_new: np.array) -> Tuple[bool, float]:

        is_in_long_tabu = not np.all(x_new[self.__long_term_tabu_list > 0])
        tabu_pl = self.__long_term_tabu_list > 0
        cadence = self.__long_term_tabu_list[(~x_new * tabu_pl) == -1] if is_in_long_tabu else 0

        return is_in_long_tabu, float(cadence)

    def __change_times_to_left_tl(self):

        self.__tabu_list[self.__tabu_list > 0] -= 1

    def __change_times_to_left_lt_tl(self):

        self.__long_term_tabu_list[self.__long_term_tabu_list > 0] -= 1

    def __delete_given_move_from_tabu(self, to_delete: np.array):

        self.__tabu_list[to_delete] = 0

    def __delete_given_move_from_long_term_tabu(self, to_delete: np.array):

        self.__long_term_tabu_list[to_delete] = 0

    def __add_move_to_tabu_list(self, move: np.array, time_to_stay_in_tl: int = None):

        if time_to_stay_in_tl is None:
            time_to_stay_in_tl = self.__min_time_in_tl

        self.__tabu_list[move == 1] = time_to_stay_in_tl

    def __add_move_to_long_term_tabu_list(self, move: np.array, time_to_stay_in_lt_tl: int = None):

        if time_to_stay_in_lt_tl is None:
            time_to_stay_in_lt_tl = self.__min_time_in_lt_tl

        self.__long_term_tabu_list[move == -1] = time_to_stay_in_lt_tl

    def __aspiration_criteria(self) -> bool:

        return self.__Q_min_new_tabu < self.__Q_min

    def __is_solution_allowed(self, solution: np.array) -> bool:
        return self.__condition_tester.is_solution_allowed(solution)

    def __stop_condition(self) -> bool:

        if self.__time_lim:
            if self.__curr_time > self.__time_lim:
                return True
            else:
                return False
        if self.__iteration_lim:
            if self.__curr_it >= self.__iteration_lim:
                return True
            else:
                return False


        logging.info("Wystąpił błąd w badaniu kryterium stopu")
        return True


if __name__ == "__main__":
    sol = Solver(n_max=1,
                 p_max=1,
                 d_max=1,
                 r=1,
                 min_time_in_tl=1,
                 min_time_in_lt_tl=1,
                 client_map=np.array([1]),

                 iteration_lim=1)

    tel = Telemetry()
    pass
