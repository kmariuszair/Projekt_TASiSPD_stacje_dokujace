import unittest
import numpy as np

import src.SolutionGrader as SolutionGrader


class TestSolutionGrader(unittest.TestCase):

    def test_find_nearest_case_1(self):

        pl_map = np.array([
            [0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
            [1, 0, 0, 0]
        ])

        clients_map = np.array([
            [1, 1, 2, 3],
            [4, 5, 5, 0],
            [0, 0, 2, 1],
            [1, 2, 3, 4]
        ])

        grader = SolutionGrader.SolutionGrader(clients_map, pl_map)

        self.assertTupleEqual((1, 2), grader._SolutionGrader__find_nearest_pl((3, 3)))

    def test_find_nearest_case_2(self):

        pl_map = np.array([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 1]
        ])

        clients_map = np.array([
            [1, 1, 2, 3],
            [4, 5, 5, 0],
            [0, 0, 2, 1],
            [1, 2, 3, 4]
        ])

        grader = SolutionGrader.SolutionGrader(clients_map, pl_map)

        self.assertTupleEqual((3, 3), grader._SolutionGrader__find_nearest_pl((0, 0)))

    def test_find_nearest_case_3(self):

        pl_map = np.array([
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ])

        clients_map = np.array([
            [1, 1, 2, 3],
            [4, 5, 5, 0],
            [0, 0, 2, 1],
            [1, 2, 3, 4]
        ])

        grader = SolutionGrader.SolutionGrader(clients_map, pl_map)

        self.assertTupleEqual((0, 1), grader._SolutionGrader__find_nearest_pl((2, 1)))

    def test_map_clients_to_pl_case_1(self):

        pl_map = np.array([
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 0],
            [1, 0, 0, 0]
        ])

        clients_map = np.array([
            [1, 1, 2, 3],
            [4, 5, 5, 0],
            [0, 0, 2, 1],
            [1, 2, 3, 4]
        ])

        expected = np.array([
            [0,13, 0, 0],
            [0, 0, 0,15],
            [0, 0, 0, 0],
            [6, 0, 0, 0]
        ])

        grader = SolutionGrader.SolutionGrader(clients_map, pl_map)
        got = grader._SolutionGrader__map_clients_to_nearest_pl()

        np.testing.assert_array_equal(expected, got)

    def test_grade_case_1(self):

        pl_map = np.array([
            [0, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 0],
            [1, 0, 0, 1]
        ])

        clients_map = np.array([
            [1, 1, 2, 3],
            [4, 5, 5, 0],
            [0, 0, 2, 1],
            [1, 2, 3, 4]
        ])

        expected = np.var([19, 8, 7])

        grader = SolutionGrader.SolutionGrader(clients_map, pl_map)
        got = grader.grade_solution(pl_map, clients_map)

        self.assertEqual(expected, got)
