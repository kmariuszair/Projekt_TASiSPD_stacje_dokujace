import numpy as np
import cv2
allowed_positions_map = cv2.imread('plan.bmp')
allowed_positions_map = cv2.cvtColor(allowed_positions_map, cv2.COLOR_BGR2GRAY)

docking_stations_map = cv2.imread('start.bmp')
docking_stations_map = cv2.cvtColor(docking_stations_map, cv2.COLOR_BGR2GRAY)


np.save('barriers.npy', allowed_positions_map)
np.save('init_docking_stations.npy', docking_stations_map)