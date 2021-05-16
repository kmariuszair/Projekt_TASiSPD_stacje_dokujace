"""
Generator mapy do znalezienia optymalnego rozmieszczenia stacji dokujących za pomocą tabu-search.
"""
from typing import List
import RobotModel


class TrafficMapGenerator:

    def __init__(self, allowed_positions_map: np.array, robots_swarm: RobotsSwarm):
        self.__allowed_positions = allowed_positions_map
        self.__robots_swarm = robots_swarm

    def generate_map(self):
        """
        Generacja mapy.
        Właściwie jest to symulacja działania robotów w magazynie/szklarni. Losowo wybierane są  obciążenia oraz
        kierunki ruchu robotów. Tutaj roboty są sterowane. Jeśli ich poziom baterii jest niski, to kierowane są do
        najbliższej stacji ładującej
        """
        pass


def generate_random_settings(settings_number: int, allowed_positions_map: np.array):
    """
    Generowanie losowych parametrów robotów
    """
    for _ in range(settings_number):
        battery_size = np.random.randi(100, 200)
        starting_battery_level = np.random.randi(100, battery_size)
        max_load = np.random.randi(5, 20)
        x0, y0 = np.random.randi(0, allowed_positions_map.shape[0]), np.random.randi(0, allowed_positions_map.shape[1])
        while allowed_positions_map[x0, y0] != 1:
            x0, y0 = np.random.randi(0, allowed_positions_map.shape[0]), np.random.randi(0,
                                                                                         allowed_positions_map.shape[1])
        starting_position = np.array([x0, y0])
        yield RobotModel.RobotSettings(battery_size, starting_battery_level, max_load, starting_position)


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

    def __init__(self, robots_number: int, allowed_positions_map: np.array):
        self.robots_list = generate_swarm(robots_number, allowed_positions_map, settings_list=predefined_settings)

    def __getitem__(self, item):
        """
        Nadpisanie []
        """
        return self.robots_list[item]

