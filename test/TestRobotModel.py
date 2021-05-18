import unittest
import numpy as np

from src.RobotModel import RobotSettings, RobotState, Robot


class TestRobotSetting(unittest.TestCase):

    def test_init(self):
        battery_size = 10
        starting_battery_level = 4
        max_load = 3
        starting_position = np.array([10, 12])
        id = 5

        robot_settings = RobotSettings(battery_size, starting_battery_level, max_load, starting_position, id)

        self.assertEqual(robot_settings.battery_size, battery_size)
        self.assertEqual(robot_settings.starting_battery_level, starting_battery_level)
        self.assertEqual(robot_settings.max_load, max_load)
        self.assertEqual(robot_settings.starting_position[0], starting_position[0])
        self.assertEqual(robot_settings.starting_position[1], starting_position[1])
        self.assertEqual(robot_settings.id, id)


class TestRobotState(unittest.TestCase):

    def test_normal_activity(self):
        battery_size = 10
        starting_battery_level = 4
        max_load = 3
        starting_position = np.array([10, 12])
        id = 5

        robot_settings = RobotSettings(battery_size, starting_battery_level, max_load, starting_position, id)

        robot_state = RobotState(robot_settings)

        direction = np.array([1, 0])
        new_load = 1
        loading_speed = 0
        robot_state.update_state(direction, new_load, loading_speed)

        self.assertEqual(robot_state.battery_level, starting_battery_level)
        self.assertEqual(robot_state.actual_load, new_load)
        self.assertEqual(robot_state.is_loading, False)
        self.assertEqual(robot_state.failure, False)
        self.assertEqual(robot_state.battery_low, False)
        self.assertEqual(robot_state.actual_position[0], starting_position[0] + direction[0])
        self.assertEqual(robot_state.actual_position[1], starting_position[1] + direction[1])

        robot_state.update_state(direction, 0, 0)
        robot_state.update_state(direction, 0, 0)
        robot_state.update_state(direction, 0, 0)

        self.assertEqual(robot_state.battery_level, 1)
        self.assertEqual(robot_state.failure, False)
        self.assertEqual(robot_state.battery_low, True)

        robot_state.update_state(direction, 0, 0)
        robot_state.update_state(direction, 0, 0)

        self.assertEqual(robot_state.battery_level, -1)
        self.assertEqual(robot_state.failure, True)
        self.assertEqual(robot_state.battery_low, True)


class TestRobot(unittest.TestCase):
    pass