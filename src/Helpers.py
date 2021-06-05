import numpy as np
from typing import Tuple, Dict


def diamond(r: int) -> np.array:
    # *...*2 sprawia, że dany argument jest przekazywany jako pierwszy i
    # drugi argument funkcji
    return np.add.outer(*[np.r_[:r, r:-1:-1]]*2) >= r


def diamond_edge(r: int) -> np.array:
    return np.add.outer(*[np.r_[:r, r:-1:-1]]*2) == r


def generate_docking_stations_map(allowed_positions: np.array, docks_no: int, frame_size: int, docks_params=None) -> np.array:
    """
    Generacja mapy stacji dokujących

    TESTED ✓
    """
    map_shape = allowed_positions.shape
    map = np.zeros(map_shape)
    investment_cost = 0
    for _ in range(docks_no):
        written = False
        # alist = [arr[0, :-1], arr[:-1, -1], arr[-1, 1:], arr[1:, 0]]
        while not written:
            tst = np.random.randint(0, 4)
            if tst == 0:
                ind = np.random.randint(0, map.shape[1] - frame_size - 1)
                ind2 = np.random.randint(0, frame_size)
                if map[:-frame_size, :-frame_size][ind2, ind] + allowed_positions[:-frame_size, :-frame_size][ind2, ind] == 0:
                    map[:-frame_size, :-frame_size][ind2, ind] = np.random.randint(10, 100)
                    investment_cost += (ind + ind2) * map[:-frame_size, :-frame_size][ind2, ind] / 100
                    written = True
            elif tst == 1:
                ind =  np.random.randint(0, map.shape[0] - frame_size - 1)
                ind2 = np.random.randint(0, frame_size)
                if map[:-frame_size, -frame_size:][ind, ind2] + allowed_positions[:-frame_size, -frame_size:][ind, ind2] == 0:
                    map[:-frame_size, -frame_size:][ind, ind2] = np.random.randint(10, 100)
                    investment_cost += (ind + ind2) * map[:-frame_size, -frame_size:][ind, ind2] / 100
                    written = True
            elif tst == 2:
                ind = np.random.randint(0, map.shape[1] - frame_size - 1)
                ind2 = np.random.randint(0, frame_size)
                if map[-frame_size:, frame_size:][ind2, ind] + allowed_positions[-frame_size:, frame_size:][ind2, ind] == 0:
                    map[-frame_size:, frame_size:][ind2, ind] = np.random.randint(10, 100)
                    investment_cost += (ind + ind2) * map[-frame_size:, frame_size:][ind2, ind] / 100
                    written = True
            elif tst == 3:
                ind = np.random.randint(0, map.shape[1] - frame_size - 1)
                ind2 = np.random.randint(0, frame_size)
                if map[frame_size:, :frame_size][ind, ind2] + allowed_positions[frame_size:, :frame_size][ind, ind2] == 0:
                    map[frame_size:, :frame_size][ind, ind2] = np.random.randint(10, 100)
                    investment_cost += (ind + ind2) * map[frame_size:, :frame_size][ind, ind2] / 100
                    written = True
    return map, investment_cost


def mix_docking_stations_map(old_map: np.array, frame_size: int) -> np.array:
    map = np.zeros(old_map.shape)
    for _, el in np.ndenumerate(old_map):
        if el == 0:
            continue
        written = False
        # alist = [arr[0, :-1], arr[:-1, -1], arr[-1, 1:], arr[1:, 0]]
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
            # alist = [arr[0, :-1], arr[:-1, -1], arr[-1, 1:], arr[1:, 0]]
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
