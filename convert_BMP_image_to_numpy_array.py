"""
    Skrypt do szybkiej konwersji obrazów zapisanych w formacie bmp 24bit (color) na macierz numpy i 
    zapisanie ich do odpowiednio nazwanych plików zgodnie z obowiązującą normą nazewnictwa. 
"""
import numpy as np
import cv2
allowed_positions_map = cv2.imread('plan.bmp')           # Read image
allowed_positions_map = cv2.cvtColor(allowed_positions_map, cv2.COLOR_BGR2GRAY) # Convert to GRAY

docking_stations_map = cv2.imread('start.bmp')           # Read image
docking_stations_map = cv2.cvtColor(docking_stations_map, cv2.COLOR_BGR2GRAY) # Convert to GRAY


np.save('barriers.npy', allowed_positions_map)
np.save('init_docking_stations.npy', docking_stations_map)