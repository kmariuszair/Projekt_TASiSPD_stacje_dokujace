"""
Implementacja modelu robota. Służy do generowania mapy.
"""
import numpy as np


class Robot:

    def __init__(self, settings: RobotSettings):
        self.__settings = settings
        self.__state = RobotState(self.__settings)

    def make_move(self, direction: Tuple[int, int], new_load: int, loading_speed: int):
        """
        :direction: wektor przemieszczenia
        :new_load: nowe obciążenie
        :loading_speed: prędkość ładowania (wartość dodatnia jeśli robot się ładuje, zerowa jeśli nie)
        :nearest_docking_station: najbliższa stacja dokująca
        """
        self.__state.update_state(direction, new_load, loading_speed)

    def get_actual_position(self) -> np.array:
        return self.__state.actual_position


class RobotState:

    def __init__(self, starting_settings: RobotSettings):
        """
        :starting_settings: Ustawienia początkowe robota
        """
        self.battery_size = starting_settings.battery_size
        self.battery_level = starting_settings.starting_battery_level
        self.max_load = starting_settings.max_load
        # zakładamy, że roboty nie są na początku obciążone
        self.actual_load = 0
        # oznacza usterkę (za niski poziom baterii lub zbyt duże obciążenie)
        self.failure = False
        self.battery_low = False
        self.actual_position = starting_settings.starting_position

    def update_state(self, direction: np.array, new_load: int, loading_speed: int):
        """
        :new_load: Zmiana stanu obciążenia robota (dodatnie, gdy zwiększamy obciążenie, ujemne, gdy odkładamy towar)
        """
        if not self.battery_low:
            """
            Robot w czasie normalnego działania
            """
            self.battery_level -= self.actual_load
            self.battery_level += loading_speed

            self.actual_load += new_load

            if self.battery_level <= 0 or self.actual_load > self.max_load:
                self.failure = True

            if self.battery_level < 0.15 * self.battery_size:
                self.battery_low = True

            self.actual_position += direction
        else:
            """
            Robot w stanie niskiego poziomu baterii
            """
            # obliczanie najbardziej optymalnego kierunku ruchu do najbliższej stacji dokującej odbywać się będzie
            # na wyższym poziomie, ponieważ potrzebny jest dostęp do mapy
            self.actual_position += direction


class RobotSettings:

    def __init__(self, battery_size, starting_battery_level, max_load, starting_position: np.array):
        self.battery_size = battery_size
        self.starting_battery_level = starting_battery_level
        self.max_load = max_load
        self.starting_position = starting_position
