import unittest
import numpy as np

import src.ConditionTester


class TestConditionTesterHelpers(unittest.TestCase):

    def test_are_to_many_clients_in_area_false(self):
        clients_map = np.array([
            [0, 0, 1, 2],
            [3, 5, 0, 2],
            [0, 1, 2, 4],
            [3, 2, 2, 0],
            [0, 0, 1, 1]
        ])
        proposed_pl_coords = (2, 2)
        cond_test = src.ConditionTester.OneConditionTester(p_max=20,
                                                           d_max=2,
                                                           clients_map=clients_map)

        self.assertFalse(cond_test._OneConditionTester__are_to_many_clients_in_area(proposed_pl_coords))

    def test_are_to_many_clients_in_area_true(self):
        clients_map = np.array([
            [0, 0, 1, 2],
            [3, 5, 0, 2],
            [0, 1, 2, 4],
            [3, 2, 8, 8],
            [0, 0, 1, 1]
        ])
        proposed_pl_coords = (2, 3)
        cond_test = src.ConditionTester.OneConditionTester(p_max=20,
                                                           d_max=2,
                                                           clients_map=clients_map)

        self.assertTrue(cond_test._OneConditionTester__are_to_many_clients_in_area(proposed_pl_coords))


class TestConditionTester(unittest.TestCase):

    def test_is_solution_allowed_false(self):
        clients_map = np.array([
            [0, 0, 1, 2],
            [3, 5, 0, 2],
            [0, 1, 2, 4],
            [3, 2, 2, 0],
            [0, 0, 1, 1]
        ])
        proposed_pl_map = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 1, 0, 0]
        ])
        cond_test = src.ConditionTester.OneConditionTester(p_max=20,
                                                           d_max=2,
                                                           clients_map=clients_map)

        self.assertFalse(cond_test.is_solution_allowed(proposed_pl_map))

    def test_is_solution_allowed_true(self):
        clients_map = np.array([
            [0, 0, 1, 2],
            [3, 5, 0, 2],
            [0, 1, 2, 4],
            [3, 2, 2, 0],
            [0, 0, 1, 1]
        ])
        proposed_pl_map = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 1, 0, 0]
        ])
        cond_test = src.ConditionTester.OneConditionTester(p_max=20,
                                                           d_max=2,
                                                           clients_map=clients_map)

        self.assertTrue(cond_test.is_solution_allowed(proposed_pl_map))


if __name__ == '__main__':
    unittest.main()
