"""
Generator mapy do znalezienia optymalnego rozmieszczenia stacji dokujących za pomocą tabu-search.
"""
from typing import List
import collections
import numpy as np
from copy import deepcopy

import src.RobotModel as RobotModel


def generate_random_settings(settings_number: int, allowed_positions_map: np.array):
    """
    Generowanie losowych parametrów robotów

    :settings_number: liczba ustawień do wygenerowania
    :allowed_positions_map: mapa pozycji dozwolonych --- 0 oznacza brak bariery, 1 oznacza barierę
    """
    for id in range(settings_number):
        battery_size = np.random.randint(501,
                                         1000)  # 501, bo battery_size musi byś większe od minimum z starting_battery_level
        starting_battery_level = np.random.randint(np.floor(0.5 * battery_size), battery_size)
        max_load = np.random.randint(25, 50)
        x0, y0 = np.random.randint(0, allowed_positions_map.shape[0]), np.random.randint(0,
                                                                                         allowed_positions_map.shape[1])
        while allowed_positions_map[x0, y0] == 1:  # dopóki trafiamy w przeszkodę
            x0, y0 = np.random.randint(0, allowed_positions_map.shape[0]), np.random.randint(0,
                                                                                             allowed_positions_map.shape[
                                                                                                 1])
        starting_position = np.array([x0, y0])
        size = (np.random.uniform(500,1000), np.random.uniform(500,1000), np.random.uniform(100,500))  # w, l, h
        max_loading_speed = np.random.uniform(10,20)
        weight = np.random.uniform(100,300)
        power = np.random.uniform(500,2000)
        max_speed = np.random.uniform(5,150)  # m/min
        name = str(id)
        price = np.random.randint(10, 100)

        yield RobotModel.RobotSettings(
                        battery_size=battery_size,
                        starting_battery_level=starting_battery_level,
                        max_load=max_load,
                        starting_position=starting_position,
                        id=id,
                        size=size,
                        max_loading_speed=max_loading_speed,
                        weight=weight,
                        power=power,
                        max_speed=max_speed,
                        name=name,
                        price=price)


def generate_swarm(robots_number: int, allowed_positions_map: np.array,
                   settings_list: List[RobotModel.RobotSettings] = None) -> List[RobotModel.Robot]:
    """
    Tworzenie roju robotów na podstawie listy ustawień, lub, jeśli nie jest podana, na podstawie losowych parametrów

    :robots_number: liczba robotów do wygenerowania
    :allowed_positions_map: mapa dozwolonych pozycji
    :settings_list: lista ustawień robotów (opcjonalna - gdy nie podana ustawienia są losowe)
    """
    if settings_list is None:
        settings_list = []
    robots_list = []
    if len(settings_list) == 0:
        # jeśli niezdefiniowano wcześniej listy ustawień to losuj ustawienia
        for random_setting in generate_random_settings(robots_number, allowed_positions_map):
            robots_list.append(RobotModel.Robot(random_setting))
    else:
        for setting in settings_list:
            robots_list.append(RobotModel.Robot(setting))
    return robots_list


class RobotsSwarm:

    def __init__(self, robots_number: int, allowed_positions_map: np.array,
                 predefined_settings: List[RobotModel.RobotSettings] = None):
        if predefined_settings is None:
            predefined_settings = []
        self.robots_list = generate_swarm(robots_number, allowed_positions_map, settings_list=predefined_settings)
        self.iter_count = 0

    def __getitem__(self, item):
        """
        Nadpisanie []
        """
        return self.robots_list[item]

    def __iter__(self):
        """
        Utworzenie iteratora
        """
        self.iter_count = 0
        return self

    def __next__(self):
        if self.iter_count >= len(self.robots_list):
            raise StopIteration
        else:
            robot = self.robots_list[self.iter_count]
            self.iter_count += 1
            return robot

    def get_robot_count(self):
        return len(self.robots_list)


class TrafficMapGenerator:

    def __init__(self, allowed_positions_map: np.array, docking_stations_map: np.array, robots_number: int,
                 robots_swarm: RobotsSwarm = None,
                 robots_swarm_predefined_settings: List[RobotModel.RobotSettings] = None):
        if robots_swarm_predefined_settings is None: robots_swarm_predefined_settings = []
        self.__allowed_positions = allowed_positions_map
        # użyj przekazanego roju robotów lub wygeneruj losowy
        self.__robots_swarm = robots_swarm if robots_swarm else RobotsSwarm(robots_number, allowed_positions_map,
                                                                            predefined_settings=robots_swarm_predefined_settings)
        # tam, gdzie wartości są większe od zera, tam znajdują się stacje dokujące, wartość danej komórki oznacza
        # prędkość ładowania
        self.__docking_stations_map = docking_stations_map
        self.__paths_to_docks = {}
        self.__paths_to_work = {}

        self.no_trips_to_docking_stations = 0
        self.cum_dist_to_dock_when_bat_low = 0

        self.busy_docks = np.zeros(docking_stations_map.shape, dtype=bool)

    def generate_map(self, sim_len: int):
        """
        Generacja mapy.
        Właściwie jest to symulacja działania robotów w magazynie/szklarni. Losowo wybierane są  obciążenia oraz
        kierunki ruchu robotów. Tutaj roboty są sterowane. Jeśli ich poziom baterii jest niski, to kierowane są do
        najbliższej stacji ładującej

        :sim_len: długość symulacji w iteracjach
        """
        # mapa pokazująca, gdzie jest duy ruch robotów
        traffic_map = np.zeros(self.__docking_stations_map.shape)
        # mapa pokazująca, gdzie zazwyczaj znajdują się roboty z niskim poziomem baterii
        loading_map = np.zeros(self.__docking_stations_map.shape)
        # mapa pokazująca, gdzie ewentualnie znajdują się popsute roboty
        failure_map = np.zeros(self.__docking_stations_map.shape)
        # Macierz zaweirająca pozcyje danego robota w danej iteracji
        # Skałda sie ona z wymiarów długosć iteracji x ilosć robotów x pozycja (2xint)
        robot_count = self.__robots_swarm.get_robot_count()
        robot_position = np.zeros((sim_len, robot_count, 2))

        for _ in range(sim_len):  # powtarza kroki symulacji tak długo, jak zadano
            robot_pos_sim_itr = []
            for robot in self.__robots_swarm:  # aktualizacja stanu dla każdego robota
                if robot.failure_detected():  # jeśli robot ma usterkę, to jest pomijany
                    # Zapisanie pozycji danego robota do odpowiedniej komórki w macierzy
                    r_pos = robot.get_actual_position()
                    id = robot.get_id()
                    robot_position[_, id, :] = r_pos
                    continue  # (nie zakładamy możliwości naprawy w czasie symulacji)
                elif robot.is_loading():  # jeśli robot się ładuje
                    r_pos = robot.get_actual_position()
                    robot.make_move(np.array([0, 0]), 0, self.__docking_stations_map[r_pos[0]][r_pos[1]])
                    if robot.get_battery_level() >= robot.get_battery_capacity():
                        self.busy_docks[r_pos[0]][r_pos[1]] = False
                else:  # jeśli robot jest w stanie normalnej pracy
                    if robot.battery_low():  # jeśli robot ma mało baterii
                        r_pos = robot.get_actual_position()
                        if self.__docking_stations_map[r_pos[0]][
                            r_pos[1]] > 0:  # jeśli robot przyjechał do stacji dokującej
                            if not self.busy_docks[r_pos[0]][r_pos[1]]:
                                self.busy_docks[r_pos[0]][r_pos[1]] = True
                                robot.make_move(np.array([0, 0]), 0, self.__docking_stations_map[r_pos[0]][r_pos[1]])
                            else:
                                robot.cumulative_awaiting_time += 1
                            # usuwa tymczasowo wygenerowaną ścieżkę do najbliższej stacji dokującej
                            # powinna zostać usunięta pusta lista
                            if robot.get_id() in self.__paths_to_docks.keys():
                                del self.__paths_to_docks[robot.get_id()]
                        else:  # jeśli robot ma mało baterii i musi jechać do stacji dokującej
                            r_pos = robot.get_actual_position()
                            direction = self.__direction_to_nearest_dock(robot.get_id(), r_pos)
                            robot.make_move(direction, 0, 0)
                            traffic_map[r_pos[0], r_pos[1]] += 1
                            loading_map[r_pos[0], r_pos[1]] += 1
                    elif robot.get_id() in self.__paths_to_work.keys():  # jeśli robot może wrócić do miejsca pracy
                        r_pos = robot.get_actual_position()
                        if len(self.__paths_to_work[robot.get_id()]) > 0:
                            direction = self.__direction_to_work(robot.get_id(), r_pos)
                            robot.make_move(direction, 0, 0)
                        else:
                            print("Robot wrócił do pracy")
                            del self.__paths_to_work[robot.get_id()]
                        traffic_map[r_pos[0], r_pos[1]] += 1
                        loading_map[r_pos[0], r_pos[1]] += 1
                    else:  # jeśli robot jest sprawny
                        r_pos = robot.get_actual_position()
                        direction = self.__generate_allowed_move(r_pos)
                        random_load = np.random.randint(-1, 2)
                        robot.make_move(direction, random_load, 0)
                        traffic_map[r_pos[0], r_pos[1]] += 1
                # Zapisanie pozycji danego robota do odpowiedniej komórki w macierzy
                r_pos = robot.get_actual_position()
                id = robot.get_id()
                robot_position[_, id, :] = r_pos

        for robot in self.__robots_swarm:
            if robot.failure_detected():
                r_pos = robot.get_actual_position()
                failure_map[r_pos[0], r_pos[1]] += 1

        # TODO: dodać to do return
        cumulative_gain = 0
        cumulative_loading_times = 0
        cumulative_awaiting_times = 0
        for robot in self.__robots_swarm:
            cumulative_gain += robot.netto_gain
            cumulative_loading_times += robot.cumulative_loading_time
            cumulative_awaiting_times += robot.cumulative_awaiting_time

        return traffic_map, loading_map, failure_map, robot_position, \
               cumulative_gain, cumulative_loading_times, cumulative_awaiting_times, \
               self.cum_dist_to_dock_when_bat_low, self.no_trips_to_docking_stations

    def __generate_allowed_move(self, actual_position):
        vmax = self.__allowed_positions.shape[0]
        hmax = self.__allowed_positions.shape[1]
        random_move = np.random.randint(-1, 2, 2)
        new_v = actual_position[0] + random_move[0]
        new_h = actual_position[1] + random_move[1]
        while not (0 <= new_v < vmax and 0 <= new_h < hmax):
            random_move = np.random.randint(-1, 2, 2)
            new_v = actual_position[0] + random_move[0]
            new_h = actual_position[1] + random_move[1]
        while self.__allowed_positions[actual_position[0] + random_move[0]][actual_position[1] + random_move[1]] == 1:
            random_move = np.random.randint(-1, 2, 2)
            new_v = actual_position[0] + random_move[0]
            new_h = actual_position[1] + random_move[1]
            while not (0 <= new_v < vmax and 0 <= new_h < hmax):
                random_move = np.random.randint(-1, 2, 2)
                new_v = actual_position[0] + random_move[0]
                new_h = actual_position[1] + random_move[1]
        return random_move

    def __direction_to_nearest_dock(self, robot_id: int, robot_position: np.array):
        if robot_id not in self.__paths_to_docks.keys():
            # odwrotna indeksacja, najpierw podany numer kolumny a potem wiersza, wartości też zwracane w odwrotnej indeksacji
            self.__paths_to_docks[robot_id] = self.__bfs((robot_position[1], robot_position[0]))
            self.__paths_to_work[robot_id] = deepcopy(self.__paths_to_docks[robot_id])
            self.__paths_to_work[robot_id].reverse()
            self.no_trips_to_docking_stations += 1
            self.cum_dist_to_dock_when_bat_low += len(self.__paths_to_docks[robot_id])

        path = self.__paths_to_docks[robot_id]
        try:
            next_point = path.pop(
                0)  # może się zdarzyć 'pop from empty list', gdy robot będzie już na miejscu stacji dokującej
            xdiff, ydiff = next_point[1] - robot_position[0], next_point[0] - robot_position[1]  # coś nie tak
            return np.array([xdiff, ydiff])
        except IndexError:
            return np.array([0, 0])

    def __direction_to_work(self, robot_id: int, robot_position: np.array):
        path = self.__paths_to_work[robot_id]
        try:
            next_point = path.pop(
                0)  # może się zdarzyć 'pop from empty list', gdy robot będzie już na miejscu stacji dokującej
            xdiff, ydiff = next_point[1] - robot_position[0], next_point[0] - robot_position[1]  # coś nie tak
            return np.array([xdiff, ydiff])
        except IndexError:
            return np.array([0, 0])

    def __bfs(self, start):
        """
        Znajdowanie ścieżki do najbliższej stacji ładującej. Zwraca listę krotek określających indeksy pozycji.
        Trzeba uważać, bo zwraca indeksy w odwrotnej kolejnosci, niż przyjmuje je numpy.array.
        Algorytm uwzględnia ograniczenia w postaci barier oraz istnienie wielu stacji ładujących.

        :start: krotka zawierająca współrzędne punktu startowego (x0, y0)
        """
        grid = self.__allowed_positions
        width = grid.shape[1]
        height = grid.shape[0]
        queue = collections.deque([[start]])
        start = (start[0], start[1])
        seen = set(tuple([start]))
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            if self.__docking_stations_map[y][x] >= 1:
                return path
            for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] != 1 and (x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))
        raise RuntimeError("Nie można odnaleźć najbliższej stacji dokującej")
