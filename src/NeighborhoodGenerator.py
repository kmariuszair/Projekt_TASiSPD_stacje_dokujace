import numpy as np


def neighborhood_generator(parcel_locker_matrix: np.array, r: int):
    """
    Generator w języku python (możemy iterować po tej funkcji - np. [n for n in neighborhood_generator(m,r)] utworzy
    listę z sąsiadzami znajdującymi się w promieniu r od rozwiązania m)

    Kolejność generowanych elementów z sąsiedztwa nie ma znaczenia.
    Zwracane elementy mogą się nawet powtarzać, ale lepiej ominąć takie sytuacje
    ponieważ traci się moc obliczeniową.

    Przykład działania:

    Dla rozwiązania początkowego:
    |0 1 0 0|
    |0 0 1 0|
    |0 0 0 0|
    i promienia 1 r=1

    Generowane są w dowolnej kolejności następujące elementy:
    |1 0 0 0| |0 0 1 0| |0 0 0 0| |0 0 0 0|
    |0 0 1 0| |0 0 1 0| |0 1 1 0| |1 0 1 0|
    |0 0 0 0| |0 0 0 0| |0 0 0 0| |0 0 0 0|

    |0 1 1 0| |0 1 0 1| |0 1 0 0| |0 1 0 0| |0 1 0 0| |0 1 0 0| |0 1 0 0|
    |0 0 0 0| |0 0 0 0| |0 0 0 1| |0 0 0 0| |0 0 0 0| |0 0 0 0| |0 1 0 0|
    |0 0 0 0| |0 0 0 0| |0 0 0 0| |0 0 0 1| |0 0 1 0| |0 1 0 0| |0 0 0 0|

    :param parcel_locker_matrix: macierz paczkomatów
    :param r:
    :return neighbor:
    """
    x_size = parcel_locker_matrix.shape[0]
    y_size = parcel_locker_matrix.shape[1]

    neighbor = np.copy(parcel_locker_matrix)

    for x in range(x_size):
        for y in range(y_size):
            if parcel_locker_matrix[x, y] == 1:
                neighbor[x, y] = 0
                for _x in range(x - r, x + r + 1):
                    for _y in range(y - r, y + r + 1):
                        if 0 <= _x <= x_size - 1 and 0 <= _y <= y_size - 1 and parcel_locker_matrix[_x, _y] == 0:
                            neighbor[_x, _y] = 1
                            yield np.copy(neighbor)
                            neighbor[_x, _y] = 0
                neighbor[x, y] = 1
