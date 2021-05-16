"""
Generator mapy do znalezienia optymalnego rozmieszczenia stacji dokujących za pomocą tabu-search.
"""
from typing import List
import collections
import numpy as np


import RobotModel


def generate_random_settings(settings_number: int, allowed_positions_map: np.array):
    """
    Generowanie losowych parametrów robotów
    """
    for id in range(settings_number):
        battery_size = np.random.randint(100, 200)
        starting_battery_level = np.random.randint(100, battery_size)
        max_load = np.random.randint(5, 20)
        x0, y0 = np.random.randint(0, allowed_positions_map.shape[0]), np.random.randint(0, allowed_positions_map.shape[1])
        while allowed_positions_map[x0, y0] != 1:
            x0, y0 = np.random.randint(0, allowed_positions_map.shape[0]), np.random.randint(0,
                                                                                         allowed_positions_map.shape[1])
        starting_position = np.array([x0, y0])
        yield RobotModel.RobotSettings(battery_size, starting_battery_level, max_load, starting_position, id)


def generate_swarm(robots_number: int, allowed_positions_map: np.array,
                   settings_list: List[RobotModel.RobotSettings] = []) -> List[RobotModel.Robot]:
    """
    Tworzenie roju robotów na podstawie listy ustawień, lub, jeśli nie jest podana, na podstawie losowych parametrów
    """
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
        self.robots_list = generate_swarm(robots_number, allowed_positions_map, settings_list=predefined_settings)
        self.iter_count = 0

    def __getitem__(self, item):
        """
        Nadpisanie []
        """
        return self.robots_list[item]

    def __iter__(self):
        self.iter_count = 0
        return self

    def __next__(self):
        if self.iter_count >= len(self.robots_list):
            raise StopIteration
        else:
            robot = self.robots_list[self.iter_count]
            self.iter_count += 1
            return robot


class TrafficMapGenerator:

    def __init__(self, allowed_positions_map: np.array, docking_stations_map: np.array, robots_number: int,
                 robots_swarm: RobotsSwarm= None):
        self.__allowed_positions = allowed_positions_map
        # użyj przekazanego roju robotów lub wygeneruj losowy
        self.__robots_swarm = robots_swarm if robots_swarm else RobotsSwarm(robots_number, allowed_positions_map)
        # tam, gdzie wartości są większe od zera, tam znajdują się stacje dokujące, wartość danej komórki oznacza
        # prędkość ładowania
        self.__docking_stations_map = docking_stations_map
        self.__paths_to_docks = {}

    def generate_map(self, sim_len: int):
        """
        Generacja mapy.
        Właściwie jest to symulacja działania robotów w magazynie/szklarni. Losowo wybierane są  obciążenia oraz
        kierunki ruchu robotów. Tutaj roboty są sterowane. Jeśli ich poziom baterii jest niski, to kierowane są do
        najbliższej stacji ładującej

        :sim_len: długość symulacji w iteracjach
        """
        traffic_map = np.zeros(self.__docking_stations_map.shape)
        for _ in range(sim_len):  # powtarza kroki symulacji tak długo, jak zadano
            for robot in self.__robots_swarm:  # aktualizacja stanu dla każdego robota
                if robot.failure_detected():  # jeśli robot ma usterkę, to jest pomijany
                    continue                  # (nie zakładamy możliwości naprawy w czasie symulacji)
                elif robot.is_loading():
                    r_pos = robot.get_actual_position()
                    robot.make_move(np.array([0, 0]), 0, self.__docking_stations_map[r_pos[0]][r_pos[1]])
                else:
                    if robot.battery_low():  # jeśli robot ma mało baterii
                        r_pos = robot.get_actual_position()
                        if self.__docking_stations_map[r_pos[0]][r_pos[1]] > 0:
                            robot.make_move(np.array([0, 0]), 0, self.__docking_stations_map[r_pos[0]][r_pos[1]])
                            # usuwa tymczasowo wygenerowaną ścieżkę do najbliższej stacji dokującej
                            # powinna zostać usunieta pusta lista
                            del self.__paths_to_docks[robot.get_id()]
                        else:
                            r_pos = robot.get_actual_position()
                            direction = self.__goto_nearest_dock(robot.get_id(), r_pos)
                            robot.make_move(direction, 0, 0)
                            traffic_map[r_pos[0], r_pos[1]] += 1
                    else:  # jeśli robot jest sprawny
                        r_pos = robot.get_actual_position()
                        direction = self.__generate_allowed_move(r_pos)
                        random_load = np.random.randint(-5, 5)
                        robot.make_move(direction, random_load, 0)
                        traffic_map[r_pos[0], r_pos[1]] += 1
        return traffic_map

    def __generate_allowed_move(self, actual_position):
        random_move = np.random.randint(-1,2, 2)
        while self.__allowed_positions[actual_position[0]+random_move[0]][actual_position[1]+random_move[1]] != 0:
            random_move = np.random.randint(-1, 2, 2)
        return random_move

    def __goto_nearest_dock(self, robot_id: int, robot_position: np.array):
        if robot_id not in self.__paths_to_docks.keys():
            self.__paths_to_docks[robot_id] = self.__bfs(robot_position)

        path = self.__paths_to_docks[robot_id]
        next_point = path.pop(0)
        xdiff, ydiff = robot_position[0] - next_point[1], robot_position[1] - next_point[0]
        return np.array([xdiff, ydiff])

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
        seen = set([start])
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            if self.__docking_stations_map[y][x] == 1:
                return path
            for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] != 1 and (x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))
        raise RuntimeError("Nie można odnaleźć najbliższej stacji dokującej")
