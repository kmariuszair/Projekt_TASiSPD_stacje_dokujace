import numpy as np


def diamond(r: int) -> np.array:
    # *...*2 sprawia, że dany argument jest przekazywany jako pierwszy i
    # drugi argument funkcji
    return np.add.outer(*[np.r_[:r, r:-1:-1]]*2) >= r


def diamond_edge(r: int) -> np.array:
    return np.add.outer(*[np.r_[:r, r:-1:-1]]*2) == r
