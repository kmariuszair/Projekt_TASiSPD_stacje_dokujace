import numpy as np
from typing import Tuple, Dict
import src.RobotModel as RobotModel


def diamond(r: int) -> np.array:
    # *...*2 sprawia, że dany argument jest przekazywany jako pierwszy i
    # drugi argument funkcji
    return np.add.outer(*[np.r_[:r, r:-1:-1]]*2) >= r


def diamond_edge(r: int) -> np.array:
    return np.add.outer(*[np.r_[:r, r:-1:-1]]*2) == r

def make_robot_setting_from_dict(dct):
    return RobotModel.RobotSettings(
                 battery_size=dct['battery_size'],
                 starting_battery_level=dct['starting_battery_level'],
                 max_load=dct['max_load'],
                 starting_position=dct['starting_position'],
                 id=dct['id'],
                 size=dct['size'],
                 max_loading_speed=dct['max_loading_speed'],
                 weight=dct['weight'],
                 power=dct['power'],
                 max_speed=dct['max_speed'],
                 name=dct['name'],
                 price=dct['price'])

def generate_docking_stations_map(allowed_positions: np.array, docks_no: int, frame_size: int, docks_params=None) -> np.array:
    """
    Generacja mapy stacji dokujących

    TESTED ✓
    """
    map_shape = allowed_positions.shape
    map = np.zeros(map_shape)
    investment_cost = 0
    maintenance_costs = 0
    docks_params_in = docks_params
    if docks_params_in is not None:
        for _, dock_param in zip(range(docks_no), docks_params_in.values()):
            map[dock_param['position']] = dock_param['loading_speed']
            investment_cost += dock_param['price'] + (dock_param['position'][0] + dock_param['position'][1])
            maintenance_costs += dock_param['loading_speed'] / 20 + (dock_param['position'][0] + dock_param['position'][1]) / 100 + 5
    else:
        for _ in range(docks_no):
            written = False
            # if dock_param:
            #     map = np.zeros(map_shape)
            #     investment_cost = 0
            #     maintenance_costs = 0
            while not written:
                tst = np.random.randint(0, 4)
                if tst == 0:
                    ind = np.random.randint(0, map.shape[1] - frame_size - 1)
                    ind2 = np.random.randint(0, frame_size)
                    if map[:-frame_size, :-frame_size][ind2, ind] + allowed_positions[:-frame_size, :-frame_size][ind2, ind] == 0:
                        map[:-frame_size, :-frame_size][ind2, ind] = np.random.randint(10, 100)
                        investment_cost += (ind + map.shape[0] - frame_size + ind2) + map[:-frame_size, :-frame_size][ind2, ind]
                        maintenance_costs += map[:-frame_size, :-frame_size][ind2, ind] / 20 + (ind + map.shape[0] - frame_size + ind2) / 100 + 5
                        written = True
                elif tst == 1:
                    ind =  np.random.randint(0, map.shape[0] - frame_size - 1)
                    ind2 = np.random.randint(0, frame_size)
                    if map[:-frame_size, -frame_size:][ind, ind2] + allowed_positions[:-frame_size, -frame_size:][ind, ind2] == 0:
                        map[:-frame_size, -frame_size:][ind, ind2] = np.random.randint(10, 100)
                        investment_cost += (ind + frame_size + ind2 + map_shape[1] - frame_size) + map[:-frame_size, -frame_size:][ind, ind2]
                        maintenance_costs += map[:-frame_size, -frame_size:][ind, ind2] / 20 + (ind + frame_size + ind2 + map_shape[1] - frame_size) / 100 + 5
                        written = True
                elif tst == 2:
                    ind = np.random.randint(0, map.shape[1] - frame_size - 1)
                    ind2 = np.random.randint(0, frame_size)
                    if map[-frame_size:, frame_size:][ind2, ind] + allowed_positions[-frame_size:, frame_size:][ind2, ind] == 0:
                        map[-frame_size:, frame_size:][ind2, ind] = np.random.randint(10, 100)
                        investment_cost += (ind + frame_size + ind2) + map[-frame_size:, frame_size:][ind2, ind]
                        maintenance_costs += map[-frame_size:, frame_size:][ind2, ind] / 20 + (ind + frame_size + ind2) / 100 + 5
                        written = True
                elif tst == 3:
                    ind = np.random.randint(0, map.shape[1] - frame_size - 1)
                    ind2 = np.random.randint(0, frame_size)
                    if map[frame_size:, :frame_size][ind, ind2] + allowed_positions[frame_size:, :frame_size][ind, ind2] == 0:
                        map[frame_size:, :frame_size][ind, ind2] = np.random.randint(10, 100)
                        investment_cost += (ind + ind2) + map[frame_size:, :frame_size][ind, ind2]
                        maintenance_costs += map[frame_size:, :frame_size][ind, ind2] / 20 + (ind + ind2) / 100 + 5
                        written = True
    return map, investment_cost, maintenance_costs


def mix_docking_stations_map(old_map: np.array, frame_size: int) -> np.array:
    map = np.zeros(old_map.shape)
    for _, el in np.ndenumerate(old_map):
        if el == 0:
            continue
        written = False
        while not written:
            tst = np.random.randint(0, 4)
            if tst == 0:
                for _ in range(frame_size * old_map.shape[1]):
                    ind = np.random.randint(0, map.shape[1]-1)
                    if map[0, :-frame_size][ind] == 0:
                        map[0, :-frame_size][ind] = el
                        written = True
            elif tst == 1:
                for _ in range(frame_size * old_map.shape[0]):
                    ind = np.random.randint(0, map.shape[0]-1)
                    if map[:-frame_size, -frame_size][ind] == 0:
                        map[:-frame_size, -frame_size][ind] = el
                        written = True
            elif tst == 2:
                for _ in range(frame_size * old_map.shape[1]):
                    ind = np.random.randint(0, map.shape[1]-1)
                    if map[-frame_size, frame_size:][ind] == 0:
                        map[-frame_size, frame_size:][ind] = el
                        written = True
            elif tst == 3:
                for _ in range(frame_size * old_map.shape[1]):
                    ind = np.random.randint(0, map.shape[1]-1)
                    if map[frame_size:, 0][ind] == 0:
                        map[frame_size:, 0][ind] = el
                        written = True
    return map


def create_docking_station_map_based_on_docks_set(map_shape: Tuple[int, int], dset: Dict[int, int], frame_size: int) -> np.array:
    """
    Generowanie mapy stacji na podstawie zadanego ich zbioru.
    :dset: zbiór (słownik) mapujący szybkość ładowania stacji na ich ilość
    """
    map = np.zeros(map_shape)
    for el in dset.keys():
        if el == 0:
            continue
        no = dset[el]
        for _ in range(no):
            written = False
            while not written:
                tst = np.random.randint(0, 4)
                if tst == 0:
                    for _ in range(frame_size * map_shape[1]):
                        ind = np.random.randint(0, map.shape[1] - 1)
                        if map[0, :-frame_size][ind] == 0:
                            map[0, :-frame_size][ind] = el
                            written = True
                elif tst == 1:
                    for _ in range(frame_size * map_shape[0]):
                        ind = np.random.randint(0, map.shape[0] - 1)
                        if map[:-frame_size, -frame_size][ind] == 0:
                            map[:-frame_size, -frame_size][ind] = el
                            written = True
                elif tst == 2:
                    for _ in range(frame_size * map_shape[1]):
                        ind = np.random.randint(0, map.shape[1] - 1)
                        if map[-frame_size, frame_size:][ind] == 0:
                            map[-frame_size, frame_size:][ind] = el
                            written = True
                elif tst == 3:
                    for _ in range(frame_size * map_shape[1]):
                        ind = np.random.randint(0, map.shape[1] - 1)
                        if map[frame_size:, 0][ind] == 0:
                            map[frame_size:, 0][ind] = el
                            written = True
    return map
