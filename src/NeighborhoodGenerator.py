import numpy as np


def neighborhood_generator(parcel_locker_matrix: np.array, r: int):
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
