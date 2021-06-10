"""
Implementacja modelu robota. Służy do generowania mapy.
"""
import numpy as np


class RobotSettings:

    def __init__(self, battery_size, starting_battery_level, max_load, starting_position: np.array, id: int):
        self.battery_size = battery_size
        self.starting_battery_level = starting_battery_level
        self.max_load = max_load
        self.starting_position = starting_position
        self.id = id


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
        self.actual_position = np.copy(starting_settings.starting_position)
        self.is_loading = False

    def update_state(self, direction: np.array, new_load: int, loading_speed: int):
        """
        :direction: kierunek ruchu
        :new_load: Zmiana stanu obciążenia robota (dodatnie, gdy zwiększamy obciążenie, ujemne, gdy odkładamy towar)
        :loading_speed: prędkość ładowania
        """
        if not self.battery_low:
            """
            Robot w czasie normalnego działania
            """
            self.battery_level -= self.actual_load
            self.battery_level += loading_speed if self.battery_level + loading_speed < self.battery_size else \
                self.battery_size - self.battery_level

            self.is_loading = True if loading_speed > 0 and self.battery_level < self.battery_size else False

            self.actual_load += new_load

            # niski stan baterii osiągany dla 30%
            if self.battery_level < 0.4 * self.battery_size:
                self.battery_low = True

            self.actual_position += direction
        elif self.is_loading:
            self.is_loading = True if loading_speed > 0 and self.battery_level < self.battery_size else False
            self.battery_low = False if not self.is_loading else True
            self.battery_level += loading_speed
        else:
            """
            Robot w stanie niskiego poziomu baterii
            """
            # obliczanie najbardziej optymalnego kierunku ruchu do najbliższej stacji dokującej odbywać się będzie
            # na wyższym poziomie, ponieważ potrzebny jest dostęp do mapy
            self.battery_level -= self.actual_load
            self.actual_position += direction
            self.is_loading = True if loading_speed > 0 and self.battery_level < self.battery_size else False

        # jeśli za bardzo obciążymy robota lub rozładujemy baterię do końca to robot wchodzi w stan usterki
        if self.battery_level <= 0 or self.actual_load > self.max_load:
            self.failure = True


class Robot:

    def __init__(self, settings: RobotSettings):
        self.__settings = settings
        self.__state = RobotState(self.__settings)

        self.netto_gain = 0  # zysk netto dla jednego robota = suma masy przewiezionych towarów
        self.cumulative_loading_time = 0  # łączny czas ładowania
        self.cumulative_awaiting_time = 0  # łączny czas oczekiwania

    def make_move(self, direction: np.array, new_load: int, loading_speed: int):
        """
        :direction: wektor przemieszczenia
        :new_load: nowe obciążenie
        :loading_speed: prędkość ładowania (wartość dodatnia jeśli robot się ładuje, zerowa jeśli nie)
        :nearest_docking_station: najbliższa stacja dokująca
        """
        if self.__state.actual_load + new_load < 0:  # gdyby się zdarzyło, że chcielibyśmy wziąć z robota więcej niż
            new_load = self.__state.actual_load      # ma załadowane
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
