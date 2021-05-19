import unittest
import numpy as np

from src.MapGenerator import generate_random_settings, generate_swarm, RobotsSwarm, TrafficMapGenerator


allowed_positions_map = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
])


class TestFunctions(unittest.TestCase):

    def test_generate_random_settings(self):

        settings_list = list()
        for _ in range(100):
            for setting in generate_random_settings(3, allowed_positions_map):
                self.assertTrue(100 <= setting.battery_size < 200)
                self.assertTrue(100 <= setting.starting_battery_level < setting.battery_size)
                self.assertTrue(5 <= setting.max_load < 20)
                self.assertTrue(allowed_positions_map[setting.starting_position[0], setting.starting_position[1]]==1)
                settings_list.append(setting)

    def test_generate_swarm__random(self):
        swarm = generate_swarm(100, allowed_positions_map)

        for robot in swarm:
            self.assertTrue(100 <= robot._Robot__settings.battery_size < 200)
            self.assertTrue(100 <= robot._Robot__settings.starting_battery_level < robot._Robot__settings.battery_size)
            self.assertTrue(5 <= robot._Robot__settings.max_load < 20)
            self.assertTrue(allowed_positions_map[robot._Robot__settings.starting_position[0], robot._Robot__settings.starting_position[1]] == 1)

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
            self.assertTrue(100 <= robot._Robot__settings.battery_size < 200)
            self.assertTrue(100 <= robot._Robot__settings.starting_battery_level < robot._Robot__settings.battery_size)
            self.assertTrue(5 <= robot._Robot__settings.max_load < 20)
            self.assertTrue(allowed_positions_map[
                                robot._Robot__settings.starting_position[0], robot._Robot__settings.starting_position[
                                    1]] == 1)

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
            self.assertTrue(100 <= robot._Robot__settings.battery_size < 200)
            self.assertTrue(100 <= robot._Robot__settings.starting_battery_level < robot._Robot__settings.battery_size)
            self.assertTrue(5 <= robot._Robot__settings.max_load < 20)
            self.assertTrue(allowed_positions_map[
                                robot._Robot__settings.starting_position[0], robot._Robot__settings.starting_position[
                                    1]] == 1)


class TestTrafficMapGenerator(unittest.TestCase):

    def test_init(self):
        pass

    def test_TrafficMapGenerator__generate_allowed_move(self):
        pass

    def test_TrafficMapGenerator__goto_nearest_dock(self):
        pass

    def test_generate_map(self):
        pass
