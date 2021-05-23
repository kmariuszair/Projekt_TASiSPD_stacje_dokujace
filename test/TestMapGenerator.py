import unittest
import numpy as np

from src.MapGenerator import generate_random_settings, generate_swarm, RobotsSwarm, TrafficMapGenerator


allowed_positions_map = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
])

docking_stations_map = np.array([
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [ 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [ 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
])


class TestFunctions(unittest.TestCase):

    def test_generate_random_settings(self):

        settings_list = list()
        for _ in range(100):
            for setting in generate_random_settings(3, allowed_positions_map):
                self.assertTrue(501 <= setting.battery_size < 1000)
                self.assertTrue(np.floor(0.5*setting.battery_size) <= setting.starting_battery_level < setting.battery_size)
                self.assertTrue(25 <= setting.max_load < 50)
                self.assertTrue(allowed_positions_map[setting.starting_position[0], setting.starting_position[1]]==0)  # 0 oznacza pozycję dozwoloną
                settings_list.append(setting)

    def test_generate_swarm__random(self):
        swarm = generate_swarm(100, allowed_positions_map)

        for robot in swarm:
            self.assertTrue(501 <= robot._Robot__settings.battery_size < 1000)
            self.assertTrue(np.floor(0.5*robot._Robot__settings.battery_size) <= robot._Robot__settings.starting_battery_level < robot._Robot__settings.battery_size)
            self.assertTrue(25 <= robot._Robot__settings.max_load < 50)
            self.assertTrue(allowed_positions_map[robot._Robot__settings.starting_position[0],
                                                  robot._Robot__settings.starting_position[1]] == 0)  # 0 oznacza pozycję dozwoloną

    def test_generate_swarm__given_settings_list(self):
        settings_list = list()
        for setting in generate_random_settings(3, allowed_positions_map):
            settings_list.append(setting)
        swarm = generate_swarm(100, allowed_positions_map, settings_list)
        for i, robot in enumerate(swarm):
            self.assertEqual(settings_list[i].battery_size, robot._Robot__settings.battery_size)
            self.assertEqual(settings_list[i].starting_battery_level, robot._Robot__settings.starting_battery_level)
            self.assertEqual(settings_list[i].max_load, robot._Robot__settings.max_load)
            self.assertTrue(np.all(settings_list[i].starting_position==robot._Robot__settings.starting_position))


class TestRobotsSwarm(unittest.TestCase):

    def test_init(self):
        robot_swarm = RobotsSwarm(3, allowed_positions_map)
        for robot in robot_swarm.robots_list:
            self.assertTrue(501 <= robot._Robot__settings.battery_size < 1000)
            self.assertTrue(np.floor(0.5*robot._Robot__settings.battery_size) <= robot._Robot__settings.starting_battery_level < robot._Robot__settings.battery_size)
            self.assertTrue(25 <= robot._Robot__settings.max_load < 50)
            self.assertTrue(allowed_positions_map[
                                robot._Robot__settings.starting_position[0], robot._Robot__settings.starting_position[
                                    1]] == 0)  # 0 oznacza pozycję dozwoloną

    def test_init_given_settings(self):
        settings_list = list()
        for setting in generate_random_settings(3, allowed_positions_map):
            settings_list.append(setting)
        robot_swarm = RobotsSwarm(3, allowed_positions_map, settings_list)
        for i, robot in enumerate(robot_swarm.robots_list):
            self.assertEqual(settings_list[i].battery_size, robot._Robot__settings.battery_size)
            self.assertEqual(settings_list[i].starting_battery_level, robot._Robot__settings.starting_battery_level)
            self.assertEqual(settings_list[i].max_load, robot._Robot__settings.max_load)
            self.assertTrue(np.all(settings_list[i].starting_position==robot._Robot__settings.starting_position))

    def test_iteration(self):
        robot_swarm = RobotsSwarm(3, allowed_positions_map)
        for robot in robot_swarm:
            self.assertTrue(501 <= robot._Robot__settings.battery_size < 1000)
            self.assertTrue(np.floor(0.5*robot._Robot__settings.battery_size) <= robot._Robot__settings.starting_battery_level < robot._Robot__settings.battery_size)
            self.assertTrue(25 <= robot._Robot__settings.max_load < 50)
            self.assertTrue(allowed_positions_map[
                                robot._Robot__settings.starting_position[0], robot._Robot__settings.starting_position[
                                    1]] == 0)  # 0 oznacza pozycję dozwoloną


class TestTrafficMapGenerator(unittest.TestCase):

    def test_random_init(self):
        traffic_map_generator = TrafficMapGenerator(allowed_positions_map, docking_stations_map, 3)

    def test_given_robots_init(self):
        robot_swarm = RobotsSwarm(3, allowed_positions_map)
        traffic_map_generator = TrafficMapGenerator(allowed_positions_map, docking_stations_map, 3,
                                                    robots_swarm=robot_swarm)

    def test_given_settings_init(self):
        robots_settings_list = [setting for setting in generate_random_settings(3, allowed_positions_map)]
        traffic_map_generator = TrafficMapGenerator(allowed_positions_map, docking_stations_map, 3,
                                                    robots_swarm_predefined_settings=robots_settings_list)

    def test_TrafficMapGenerator__generate_allowed_move(self):
        small_pos_map = np.array([[1, 1, 1], [1, 0, 1], [0, 1, 1]])
        small_docs_map = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 1]])
        traffic_map_generator = TrafficMapGenerator(small_pos_map, small_docs_map, 3)
        for _ in range(100):
            direction = traffic_map_generator._TrafficMapGenerator__generate_allowed_move((1, 1))
            self.assertFalse(np.all(direction == np.array([-1, -1])))

    def test_TrafficMapGenerator__direction_to_nearest_dock(self):
        for _ in range(100):
            traffic_map_generator = TrafficMapGenerator(allowed_positions_map, docking_stations_map, 3)
            for robot in traffic_map_generator._TrafficMapGenerator__robots_swarm:
                robot_id = robot.get_id()
                robot_pos = robot.get_actual_position()
                direction = traffic_map_generator._TrafficMapGenerator__direction_to_nearest_dock(robot_id, robot_pos)

                # sprawdzam czy kierunek jest w zakresie iloczynu kartezjańskiego zbiorów <-1, 1>X<-1, 1>
                self.assertGreaterEqual(direction[0], -1)
                self.assertLessEqual(direction[0], 1)

                self.assertGreaterEqual(direction[1], -1)
                self.assertLessEqual(direction[1], 1)

                # sprawdzam, czy wygenerowała się lista punktów reprezentująca drogę do najbliższej stacji dokującej
                self.assertIsNotNone(traffic_map_generator._TrafficMapGenerator__paths_to_docks[robot_id])

    def test_generate_map(self):
        for _ in range(10):
            traffic_map_generator = TrafficMapGenerator(allowed_positions_map, docking_stations_map, 3)
            traffic_map, loading_map, failure_map = traffic_map_generator.generate_map(10000)
            self.assertEqual(np.sum(traffic_map[allowed_positions_map==1]), 0)

    def test_generate_reasonable_size(self):
        traffic_map_generator = TrafficMapGenerator(allowed_positions_map, docking_stations_map, 20)
        traffic_map, loading_map, failure_map = traffic_map_generator.generate_map(10000)
        self.assertEqual(np.sum(traffic_map[allowed_positions_map == 1]), 0)