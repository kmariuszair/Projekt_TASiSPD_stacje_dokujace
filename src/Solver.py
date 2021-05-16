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

# https://code.tutsplus.com/tutorials/write-your-own-python-decorators--cms-25630
# https://stackoverflow.com/questions/11731136/class-method-decorator-with-self-arguments
# https://dev.to/apcelent/python-decorator-tutorial-with-example-529f
class Telemetry:

    telemetry_data = {}

    telemetry_on = True

    @staticmethod
    def print_telemetry():
        """
        Formatuje i wypisuje telemetrię

        :return: None
        """
        logging.info("{:>40}".format("TELEMETRIA"))
        # Print the names of the columns.
        logging.info("{:<50} {:>15}".format('NAZWA METODY', 'CZAS [S]'))

        # print each data item.
        for key, value in zip(Telemetry.telemetry_data.keys(), Telemetry.telemetry_data.items()):
            name, comp_time = value
            logging.info("{:<50} {:>10}.{}".format(name, int(np.floor(comp_time)), int((comp_time % 1)*100)))

    @staticmethod
    def get_telemetry_data():
        return dict.copy(Telemetry.telemetry_data)

    @staticmethod
    def telemetry(method: Callable = None, class_name: str = 'Solver'):
        """
        Dekorator zapewniający przeprowadzenie telemetrii.

        :param method: przechwytywana metoda
        :param class_name: nazwa klasy, potrzebne do poprawy nazw metod prywatnych
        :return:
        """

        if method is None:
            return partial(Telemetry.telemetry)

        method_name = method.__name__
        # modyfikuje nazwę metody, żeby zgadzała się z tą z atrybutu klasy
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


# https://stackoverflow.com/questions/6307761/how-to-decorate-all-functions-of-a-class-without-typing-it-over-and-over-for-eac
def for_all_methods_and_class(decorator_cls, decorator_fun):
    def decorate(cls, *args, **kwargs):
        for attr in cls.__dict__:  # there's probably a better way to do this
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
    """
    Klasa zawierająca elementy konieczne do rozwiązania problemu
    """

    def __init__(self,
                 n_max: int,
                 p_max: int,
                 d_max: int,
                 r: int,
                 min_time_in_tl: int,
                 min_time_in_lt_tl: int,
                 client_map: np.array,

                 record_and_plot_data: bool = False,

                 time_lim: float = None,
                 iteration_lim: int = None,

                 dynamic_neighborhood: bool = True,

                 telemetry_on: bool = False,

                 starting_solution: np.array = None):
        """
        Inicjalizacja atrybutów klasy. Atrybuty te są konieczne do rozwiązania problemu.
        Wstępnie inicjalizuje zmienne, które będą potrzebne na dalszym etapie rozwiązywania problemu.

        :param n_max: ilość paczkomatów
        :param p_max: pojemność paczkomatów
        :param d_max: zasięg (promień) działania paczkomatów
        :param r: wielkość (promień) sąsiedztwa danego rozwiązania
        :param min_time_in_tl: rozmiar listy tabu
        :param client_map: wcześniej wygenerowana mapa z klientami
        :param record_and_plot_data: czy algorytm ma zbierać informacje o przebiegu algorytmu i je wyświetlać
        :param time_lim: limit czasu czas wykonywania obliczeń
        :param iteration_lim: limit iteracji algorytmu
        :param telemetry_on: czy rejestrować telemetrię
        :param starting_solution: zadane rozwiązanie startowe, możemy wykorzystać ten parametr, gdy korzystamy z
                                  innego niż standardowego generatora rozwiązania początkowego
        """

        # Atrybuty związane z parametrami problemu
        self.__n_max = n_max
        self.__p_max = p_max
        self.__d_max = d_max

        self.__r = r
        self.__min_time_in_tl = min_time_in_tl
        self.__min_time_in_lt_tl = min_time_in_lt_tl
        self.__client_map = np.copy(client_map)

        self.__condition_tester = ConditionTester.OneConditionTester(p_max=self.__p_max,
                                                                     d_max=self.__d_max,
                                                                     clients_map=self.__client_map)

        self.__record_and_plot_data = record_and_plot_data

        self.__dynamic_neighborhood = dynamic_neighborhood

        #Klasa odpowiedzialna za rejestrację i reprezentację danych zebranych podczas przebiegu algorytmu
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
            if np.sum(starting_solution) == self.__n_max and self.__is_solution_allowed(starting_solution):
                self.__starting_solution = np.copy(starting_solution)
            else:
                if self.__record_and_plot_data:
                    logging.info("Przekazane rozwiązanie początkowe nie spełnia kryteriów. Użyty zostanie domyślny generator")
                self.__starting_solution = None
        else:
            self.__starting_solution = None

        # atrybuty związane z przebiegiem algorytmu
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
            # Utwórz wykres telemetrii
            DataCollectorPlotter.generate_plot_of_telemetry(Telemetry.get_telemetry_data())
        # Reprezentacja uzyskanych danych podczas przebiegu algorytmu
        self.__collect_and_represent_data.plot_data()
        return to_return

    def __solve(self) -> np.array:
        """
        Funkcja implementuje dostosowany przez nas algorytm Tabu Search.

        :param record_and_plot_data: opcjonalny argument służący do wyboru, czy chcemy wizualizować przebieg algorytmu
        :return self.__x_min: najlepsze znalezione rozwiązanie
        """
        # inicjalizacja zmiennych odpowiedzialnych za kryterium stopu
        start_time = time.time()
        self.__curr_time = 0
        self.__curr_it = 0

        if self.__record_and_plot_data:
            logging.info("Generuję rozwiązanie początkowe")
        self.__x_a = self.__get_starting_solution()
        self.__x_min = np.copy(self.__x_a)
        self.__Q_a = self.__cost(self.__x_a)
        self.__Q_min = self.__Q_a

        logging.info("Koszt rozwiązania początkowego: {}".format(self.__Q_a))
        self.__collect_and_represent_data.collect_data(self.__x_a, self.__Q_a, self.__tabu_list,
                                                       self.__long_term_tabu_list, 0,
                                                       0, 0,
                                                       0, 0)

        while not self.__stop_condition():
            # aktualny numer iteracji, dany na sam początek w przypadku, gdyby był potrzebny aktualny indeks iteracji
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
                            # jeśli jest w krótkoterminowej liście tabu to licz średnią kadencyjność elementu, który
                            # zabrania ruch i licz ilość zabronień
                            av_cadence += cadence
                            elems_in_short_tabu += 1
                            if Q_new < self.__Q_min_new_tabu:
                                self.__Q_min_new_tabu = Q_new
                                self.__x_min_new_tabu = np.copy(x_new)
                    else:
                        # jeśli jest w długoterminowej liście tabu to licz średnią kadencyjność elementu, który
                        # zabrania ruch i licz ilość zabronień
                        av_long_cadence += long_cadence
                        elems_in_long_tabu += 1
                        if Q_new < self.__Q_min_new_tabu:
                            self.__Q_min_new_tabu = Q_new
                            self.__x_min_new_tabu = np.copy(x_new)
                if (self.__Q_min_new < 0.5 * (self.__Q_min + self.__Q_a)) and self.__dynamic_neighborhood:
                    break

            logging.info('Przeszukano ' + str(elems_in_nei) + ' elementów z sąsiedztwa')

            # licz średnie współczynniki kadencyjności elementów, które dokonały zabronienia
            av_cadence = float(av_cadence / elems_in_short_tabu if elems_in_short_tabu > 0 else self.__min_time_in_tl)
            av_long_cadence = float(av_long_cadence / elems_in_long_tabu if elems_in_long_tabu > 0 else
                                    self.__min_time_in_lt_tl)
            # normalizacja, żeby pokazywało, ile iteracji wcześniej został dodany element zabraniający
            av_cadence = self.__min_time_in_tl - av_cadence
            av_long_cadence = self.__min_time_in_lt_tl - av_long_cadence

            prev_x_a = np.copy(self.__x_a)
            self.__x_a = np.copy(self.__x_min_new) if not (self.__x_min_new is None) else None
            self.__Q_a = self.__Q_min_new

            if self.__aspiration_criteria():
                self.__x_a = np.copy(self.__x_min_new_tabu)
                self.__Q_a = self.__Q_min_new_tabu
                # zmodyfikuj odpowiednią listę tabu, na podstawie której rozwiązaniu tutaj trafiło
                if self.__is_in_long_term_tabu_list(self.__x_a)[0]:
                    # potrzebujemy jednej jedynki w miejscu, gdzie stał paczkomat, którego nie wolno było ruszyć
                    move = prev_x_a - self.__x_a
                    self.__delete_given_move_from_long_term_tabu(move == 1)
                    # jeśli jest na obu listach, to trzeba też usunąć z listy krótkoterminowej
                    # bardzo rzadko zachodzi taka sytuacja, ale gdy już do niej dojdzie to następuje błąd
                    if self.__is_in_tabu_list(self.__x_a)[0]:
                        move = (self.__tabu_list > 0) * (self.__x_a > 0)
                        self.__delete_given_move_from_tabu(move)
                else:
                    # potrzebujemy miejsca, w które nie wolno było postawić paczkomatu
                    move = (self.__tabu_list > 0) * (self.__x_a > 0)
                    self.__delete_given_move_from_tabu(move)
            if self.__Q_a < self.__Q_min:
                # należy pamiętać, że gdyby nie copy, to modyfikacja
                # x_a zmieniała by też x_min
                self.__x_min = np.copy(self.__x_a)
                self.__Q_min = self.__Q_a
            if self.__x_a is None:
                if self.__record_and_plot_data:
                    logging.info("Nie znaleziono nowego rozwiązania w sąsiedztwie")
                break

            # Dla listy tabu składającej się od razu z indeksów
            # natychmiast usunie najstarszy ruch
            self.__change_times_to_left_tl()
            self.__change_times_to_left_lt_tl()
            move = prev_x_a - self.__x_a
            self.__add_move_to_tabu_list(move)
            self.__add_move_to_long_term_tabu_list(move)

            # Aktualizacja zmiennych odpowiadających za kryterium czasowe stopu
            self.__curr_time = time.time() - start_time

            # Aktualizacja danych przekazywanych do DataCollectorPlotter
            self.__collect_and_represent_data.collect_data(self.__x_a, self.__Q_a, self.__tabu_list,
                                                           self.__long_term_tabu_list, elems_in_nei,
                                                           av_cadence, av_long_cadence,
                                                           elems_in_short_tabu, elems_in_long_tabu)
        return self.__x_min

    def __yield_neighbor(self):
        return NeighborhoodGenerator.neighborhood_generator(self.__x_a, self.__r)

    def __get_starting_solution(self):
        """
        Funkcja zwracająca rozwiązanie początkowe. Używamy jej w celu wybrania, czy rozwiązanie początkowe
        powinno być wygenerowane, czy przyjęte to z inicjalizacji klasy. Preferowane jest to z inicjalizacji.

        :return []: rozwiązanie początkowe
        """
        if not (self.__starting_solution is None):
            return self.__starting_solution
        else:
            return self.__default_starting_sol_gen.generate()

    def __cost(self, x_new: np.array) -> int:
        """
        Funkcja licząca koszt danego rozwiązania. Korzysta ze wzoru zamieszczonego w dokumentacji.

        :param x_new: rozwiązanie, dla którego liczona jest funkcja celu
        :return cost: koszt dla tego rozwiązania
        """
        cost = 0
        for index, value in np.ndenumerate(self.__client_map):
            if value > 0:
                cost += value * self.__dist_to_nearest_pl(index, x_new)

        return cost

    def __dist_to_nearest_pl(self, actual_point: Tuple[int, int], pl_map: np.array) -> int:

        """
        Funkcja zwracająca odległość pomiędzy punktem [actual_point] a najbliższym paczkomatem, jeśli ta odległość
        jest mniejsza od D_max. W przeciwnym wypadku zwraca powiększoną wartość tej najmniejszej odległości.

        :param pl_map:
        :param actual_point:
        :return:
        """
        # Wersja macierzowa - najszybszy sposób przeprowadzania obliczeń
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
        """
        Sprawdza, czy dane rozwiązanie znajduje się na liście tabu oraz zwraca współczynnik elementu zabraniającego
        ruch (jeżeli element nie znajduje sie na liście tabu to zwracana jest wartość 0 tego współczynnika)
        Robi to w następujący sposób:
        1) oblicza różnicę między macierzami x_new (reprezentującą nowe rozwiązanie)
           oraz self.__tabu_list (oznaczającej statyczną listę tabu)
        2) liczy ilość elementów dodatnich w tej macierzy oznaczającej różnicę
        3) jeśli ilość tych elementów jest mniejsza od liczby paczkomatów na mapie
           to oznacza, że dane rozwiązanie znajduje się na liście tabu
           W przeciwnym wypadku nie znajduje się na tej liście.
        Przykład:
        x_new:
        | 1 0 0 |
        | 0 0 1 |
        | 0 0 0 |
        self.__tabu_list:
        | 0 0 0 |
        | 3 1 2 |
        | 4 0 0 |
        Dla takich danych mamy:
        diff:
        | 1  0  0 |
        |-3 -1 -1 |
        |-4  0  0 |
        diff ma jeden element dodatni, jeden jest mniejsze od 2 (n_max=2)
        czyli x_new znajduje się na liście tabu

        :param x_new: nowe rozwiązanie
        :return [bool]: odpowiedź na pytanie, czy dane rozwiązanie jest czy go nie ma na liście tabu
        """
        diff = x_new - self.__tabu_list
        pl_not_in_forbidden_places = np.count_nonzero(diff > 0)

        is_in_tabu = pl_not_in_forbidden_places < self.__n_max
        cadence = self.__tabu_list[(diff <= 0) * (x_new > 0)] if is_in_tabu else 0

        return is_in_tabu, float(cadence)

    def __is_in_long_term_tabu_list(self, x_new: np.array) -> Tuple[bool, float]:
        """
        Sprawdza, czy kandydat jest na długoterminowej liście tabu.
        Długoterminowa lista tabu składa się elementów niezerowych w miejscach, w których są paczkomaty,
        których nie możemy ruszać.

        Sprawdza, czy we wszystkich polach, gdzie macierz tabu ma wartości niezerowe, są paczkomaty

        :param x_new: nowe rozwiązanie
        :return:
        """
        is_in_long_tabu = not np.all(x_new[self.__long_term_tabu_list > 0])
        tabu_pl = self.__long_term_tabu_list > 0
        cadence = self.__long_term_tabu_list[(~x_new * tabu_pl) == -1] if is_in_long_tabu else 0

        return is_in_long_tabu, float(cadence)

    def __change_times_to_left_tl(self):
        """
        Edytuje naszą listę tabu (czyli tą macierz z jedynkami, gdzie oznaczają one miejsca, w których postawiono już
        paczkomaty we wcześniejszych iteracjach).
        Z racji przyjętej formy tej listy, zmniejszenie współczynnika kadencyjności do 0 jest równoznaczne
        z wypadnięciem danego rozwiązania z listy tabu
        """
        self.__tabu_list[self.__tabu_list > 0] -= 1

    def __change_times_to_left_lt_tl(self):
        """
        Edytuje długoterminową listę tabu
        """
        self.__long_term_tabu_list[self.__long_term_tabu_list > 0] -= 1

    def __delete_given_move_from_tabu(self, to_delete: np.array):
        """
        Usuwa dany ruch z listy tabu.
        Najlepiej, gdybyśmy pod pojęciem ruchu rozumieli macierz z jedną jedynką, która oznacza komórkę,
        w której już był postawiony paczkomat

        :param to_delete: współrzędne elementu dla macierzy listy tabu, który powinien zostać usunięty (wyzerowany)
        """
        self.__tabu_list[to_delete] = 0

    def __delete_given_move_from_long_term_tabu(self, to_delete: np.array):
        """
        Usuwa miejsce paczkomatu z długoterminowej listy tabu.

        :param to_delete: współrzędne elementu dla macierzy listy tabu, który powinien zostać usunięty (wyzerowany)
        """
        self.__long_term_tabu_list[to_delete] = 0

    def __add_move_to_tabu_list(self, move: np.array, time_to_stay_in_tl: int = None):
        """
        Dodaje byłą pozycję paczkomatu do listy tabu

        :param move: współrzędne komórki, z której przeniesiono paczkomat
                    (przekazywane jako macierz z jedną wartością True)
        """
        if time_to_stay_in_tl is None:
            time_to_stay_in_tl = self.__min_time_in_tl

        self.__tabu_list[move == 1] = time_to_stay_in_tl

    def __add_move_to_long_term_tabu_list(self, move: np.array, time_to_stay_in_lt_tl: int = None):
        """
        Dodaje byłą pozycję paczkomatu do listy tabu

        :param move: współrzędne komórki, z której przeniesiono paczkomat
                    (przekazywane jako macierz z jedną wartością True)
        """
        if time_to_stay_in_lt_tl is None:
            time_to_stay_in_lt_tl = self.__min_time_in_lt_tl

        self.__long_term_tabu_list[move == -1] = time_to_stay_in_lt_tl

    def __aspiration_criteria(self) -> bool:
        """
        Zwraca wartość logiczną kryterium aspiracji
        Funkcjonalność przeniesiona do osobnej metody,
        aby móc ją w razie potrzeby rozbudowywać
        :return:
        """
        return self.__Q_min_new_tabu < self.__Q_min

    def __is_solution_allowed(self, solution: np.array) -> bool:
        return self.__condition_tester.is_solution_allowed(solution)

    def __stop_condition(self) -> bool:
        """
        Kryterium stopu.
        Uogólnia działanie tego kryterium na przypadki, kiedy ograniczeniem jest
        liczba iteracji lub czas obliczeń
        :return [bool]: wartość logiczna kryterium stopu (jeśli prawda to zakończ działanie)
        """
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

        # W przypadku wykrycia błędu, zakończ działanie algorytmu
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
