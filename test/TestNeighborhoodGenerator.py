import unittest
import numpy as np

import src.NeighborhoodGenerator


class TestNeighborhoodGenerator(unittest.TestCase):

    def test_case_from_f_description_example(self):
        r = 1
        docks_matrix = np.array([[0, 1, 0, 0],
                                         [0, 0, 1, 0],
                                         [0, 0, 0, 0]])


        n1 = np.array([[1, 0, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 0]])
        n2 = np.array([[0, 0, 1, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 0]])
        n3 = np.array([[0, 0, 0, 0],
                       [0, 1, 1, 0],
                       [0, 0, 0, 0]])
        n4 = np.array([[0, 0, 0, 0],
                       [1, 0, 1, 0],
                       [0, 0, 0, 0]])
        n5 = np.array([[0, 1, 1, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0]])
        n6 = np.array([[0, 1, 0, 1],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0]])
        n7 = np.array([[0, 1, 0, 0],
                       [0, 0, 0, 1],
                       [0, 0, 0, 0]])
        n8 = np.array([[0, 1, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 1]])
        n9 = np.array([[0, 1, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 1, 0]])
        n10 = np.array([[0, 1, 0, 0],
                       [0, 0, 0, 0],
                       [0, 1, 0, 0]])
        n11 = np.array([[0, 1, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 0, 0]])

        expected = [n1, n2, n3, n4,
                    n5, n6, n7, n8, n9, n10, n11]
        result = [n for n in src.NeighborhoodGenerator.neighborhood_generator(docks_matrix, r)]



        for n in expected:
            is_n_in_r_res = False
            for r in result:
                if np.all(n == r):
                    is_n_in_r_res = True
            if not is_n_in_r_res:
                assert False, "Result don't have one of the expected neighbors: \n" + str(n) + '\n'

        for r in result:
            is_r_in_s_res = False
            for n in expected:
                if np.all(n == r):
                    is_r_in_s_res = True
            if not is_r_in_s_res:
                assert False, "Result have additional solution, which was not expected: \n" + str(r) + '\n'

    def test_locked_pl_more_r(self):
        r = 2
        docks_matrix = np.array([[1, 1, 1, 0],
                                         [1, 1, 1, 0],
                                         [1, 1, 0, 0]])

































        expected = [
            np.array([
                [0, 1, 1, 0],
                [1, 1, 1, 0],
                [1, 1, 1, 0]
            ]),
            np.array([
                [1, 0, 1, 1],
                [1, 1, 1, 0],
                [1, 1, 0, 0]
            ]),
            np.array([
                [1, 0, 1, 0],
                [1, 1, 1, 1],
                [1, 1, 0, 0]
            ]),
            np.array([
                [1, 0, 1, 0],
                [1, 1, 1, 0],
                [1, 1, 0, 1]
            ]),
            np.array([
                [1, 0, 1, 0],
                [1, 1, 1, 0],
                [1, 1, 1, 0]
            ]),
            np.array([
                [1, 1, 0, 1],
                [1, 1, 1, 0],
                [1, 1, 0, 0]
            ]),
            np.array([
                [1, 1, 0, 0],
                [1, 1, 1, 1],
                [1, 1, 0, 0]
            ]),
            np.array([
                [1, 1, 0, 0],
                [1, 1, 1, 0],
                [1, 1, 0, 1]
            ]),
            np.array([
                [1, 1, 0, 0],
                [1, 1, 1, 0],
                [1, 1, 1, 0]
            ]),
            np.array([
                [1, 1, 1, 0],
                [0, 1, 1, 0],
                [1, 1, 1, 0]
            ]),
            np.array([
                [1, 1, 1, 1],
                [1, 0, 1, 0],
                [1, 1, 0, 0]
            ]),
            np.array([
                [1, 1, 1, 0],
                [1, 0, 1, 1],
                [1, 1, 0, 0]
            ]),
            np.array([
                [1, 1, 1, 0],
                [1, 0, 1, 0],
                [1, 1, 0, 1]
            ]),
            np.array([
                [1, 1, 1, 0],
                [1, 0, 1, 0],
                [1, 1, 1, 0]
            ]),
            np.array([
                [1, 1, 1, 1],
                [1, 1, 0, 0],
                [1, 1, 0, 0]
            ]),
            np.array([
                [1, 1, 1, 0],
                [1, 1, 0, 1],
                [1, 1, 0, 0]
            ]),
            np.array([
                [1, 1, 1, 0],
                [1, 1, 0, 0],
                [1, 1, 0, 1]
            ]),
            np.array([
                [1, 1, 1, 0],
                [1, 1, 0, 0],
                [1, 1, 1, 0]
            ]),
            np.array([
                [1, 1, 1, 0],
                [1, 1, 1, 0],
                [0, 1, 1, 0]
            ]),
            np.array([
                [1, 1, 1, 1],
                [1, 1, 1, 0],
                [1, 0, 0, 0]
            ]),
            np.array([
                [1, 1, 1, 0],
                [1, 1, 1, 1],
                [1, 0, 0, 0]
            ]),
            np.array([
                [1, 1, 1, 0],
                [1, 1, 1, 0],
                [1, 0, 0, 1]
            ]),
            np.array([
                [1, 1, 1, 0],
                [1, 1, 1, 0],
                [1, 0, 1, 0]
            ])
        ]

        result = [n for n in src.NeighborhoodGenerator.neighborhood_generator(docks_matrix, r)]

        for n in expected:
            is_n_in_r_res = False
            for r in result:
                if np.all(n == r):
                    is_n_in_r_res = True
            if not is_n_in_r_res:
                assert False, "Result don't have one of the expected neighbors: \n" + str(n) + '\n'

        for r in result:
            is_r_in_s_res = False
            for n in expected:
                if np.all(n == r):
                    is_r_in_s_res = True
            if not is_r_in_s_res:
                assert False, "Result have additional solution, which was not expected: \n" + str(r) + '\n'


if __name__ == '__main__':
    unittest.main()
