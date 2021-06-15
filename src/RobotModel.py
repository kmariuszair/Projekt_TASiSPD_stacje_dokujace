import numpy as np
from typing import Tuple


class RobotSettings:

    def __init__(self,
                 battery_size: int,
                 starting_battery_level: int,
                 max_load: int,
                 starting_position: np.array,
                 id: int,
                 size: Tuple[float, float, float],
                 max_loading_speed: float,
                 weight: float,
                 power: float,
                 max_speed: float,
                 name: str,
                 price: int):

        self.battery_size = battery_size
        self.starting_battery_level = starting_battery_level
        self.max_load = max_load
        self.starting_position = starting_position
        self.id = id
        self.size = size
        self.max_loading_speed = max_loading_speed
        self.weight = weight
        self.power = power
        self.max_speed = max_speed
        self.name = name
        self.price = price


class RobotState:

    def __init__(self, starting_settings: RobotSettings):

        self.battery_size = starting_settings.battery_size
        self.battery_level = starting_settings.starting_battery_level
        self.max_load = starting_settings.max_load

        self.actual_load = 0

        self.failure = False
        self.battery_low = False
        self.actual_position = np.copy(starting_settings.starting_position)
        self.is_loading = False

    def update_state(self, direction: np.array, new_load: int, loading_speed: int):

        if not self.battery_low:

            self.battery_level -= self.actual_load//10 + 1
            self.battery_level += loading_speed if self.battery_level + loading_speed < self.battery_size else \
                self.battery_size - self.battery_level

            self.is_loading = True if loading_speed > 0 and self.battery_level < self.battery_size else False

            self.actual_load += new_load


            if self.battery_level < 0.4 * self.battery_size:
                self.battery_low = True

            self.actual_position += direction
        elif self.is_loading:
            self.is_loading = True if loading_speed > 0 and self.battery_level < self.battery_size else False
            self.battery_low = False if not self.is_loading else True
            self.battery_level += loading_speed
        else:

            self.battery_level -= self.actual_load//20 + 1 if np.linalg.norm(direction) > 0 else 0
            self.actual_position += direction
            self.is_loading = True if loading_speed > 0 and self.battery_level < self.battery_size else False


        if self.battery_level <= 0 or self.actual_load > self.max_load:
            self.failure = True


class Robot:

    def __init__(self, settings: RobotSettings):
        self.__settings = settings
        self.__state = RobotState(self.__settings)

        self.netto_gain = 0
        self.cumulative_loading_time = 0
        self.cumulative_awaiting_time = 0

    def make_move(self, direction: np.array, new_load: int, loading_speed: int):

        if self.__state.actual_load + new_load < 0:
            new_load = self.__state.actual_load
        self.__state.update_state(direction, new_load, loading_speed)

        if new_load > 0:
            self.netto_gain += 1

        if self.__state.is_loading:
            self.cumulative_loading_time += 1

    def get_actual_position(self) -> np.array:
        return np.copy(self.__state.actual_position)

    def battery_low(self) -> bool:
        return self.__state.battery_low

    def failure_detected(self) -> bool:
        return self.__state.failure

    def get_id(self) -> int:
        return self.__settings.id

    def is_loading(self):
        return self.__state.is_loading

    def get_battery_level(self):
        return self.__state.battery_level

    def get_battery_capacity(self):
        return self.__state.battery_size
