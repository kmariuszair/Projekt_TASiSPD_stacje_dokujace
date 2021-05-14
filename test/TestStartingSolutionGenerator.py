import unittest
import numpy as np

import src.StartingSolutionGenerator as StartingSolutionGenerator


class TestStartingSolutionGenerator(unittest.TestCase):

    def test_check_client_number_in_pl_range(self):
        n_max = 1
        p_max = 1
        d_max = 1
        clients_map = np.array([
            [1, 2, 9, 1],
            [6, 3, 0, 0],
            [0, 0, 7, 5],
        ])

        gen = StartingSolutionGenerator.StartingSolutionGen(n_max,
                                                            p_max,
                                                            d_max,
                                                            clients_map)
        where = (1, 2)
        expected_clients_num = 19

        self.assertTrue(expected_clients_num, gen._StartingSolutionGen__check_client_number_in_pl_range(where))

    def test_check_client_number_in_pl_range_bigger_range(self):
        n_max = 1
        p_max = 1
        d_max = 3
        clients_map = np.array([
            [1, 2, 9, 1],
            [3, 3, 3, 0],
            [8, 0, 7, 5],
            [6, 7, 0, 2],
            [2, 8, 3, 0]
        ])

        gen = StartingSolutionGenerator.StartingSolutionGen(n_max,
                                                                p_max,
                                                                d_max,
                                                                clients_map)
        where = (3, 1)
        expected_clients_num = np.sum(clients_map) - 1 - 9 - 1

        self.assertTrue(expected_clients_num, gen._StartingSolutionGen__check_client_number_in_pl_range(where))

    def test_making_mask_matrix(self):
        n_max = 1
        p_max = 1
        d_max = 2

        clients_map = np.array([
            [3, 0, 0, 0, 2],
            [0, 0, 1, 0, 0],
            [0, 2, 0, 0, 0],
            [0, 0, 0, 1, 1]
        ])

        start_gen = StartingSolutionGenerator.StartingSolutionGen(n_max,
                                                                  p_max,
                                                                  d_max,
                                                                  clients_map)

        expected = np.array([
            [1, 3, 3, 2, 1],
            [3, 3, 2, 3, 3],
            [2, 2, 3, 4, 3],
            [1, 2, 4, 2, 2]
        ])

        start_gen._StartingSolutionGen__make_mask_matrix()

        self.assertTrue(np.all(expected == start_gen._StartingSolutionGen__mask_matrix))

    def test_making_mask_matrix_2(self):
        n_max = 1
        p_max = 1
        d_max = 1

        clients_map = np.array([
            [3, 0, 0, 0, 2],
            [2, 0, 1, 0, 0],
            [0, 2, 0, 0, 0],
            [0, 0, 2, 1, 1],
            [5, 5, 0, 0, 1],
            [1, 1, 0, 0, 0],
            [0, 0, 0, 1, 0]
        ])

        start_gen = StartingSolutionGenerator.StartingSolutionGen(n_max,
                                                                  p_max,
                                                                  d_max,
                                                                  clients_map)

        expected = np.array([
            [2, 1, 1, 1, 1],
            [2, 3, 1, 1, 1],
            [2, 1, 3, 1, 1],
            [1, 3, 2, 3, 3],
            [3, 3, 2, 2, 2],
            [3, 3, 1, 1, 1],
            [1, 1, 1, 1, 1]
        ])

        start_gen._StartingSolutionGen__make_mask_matrix()

        self.assertTrue(np.all(expected == start_gen._StartingSolutionGen__mask_matrix))

    def test_reduce_temp_clients_map(self):
        n_max = 1
        p_max = 1
        d_max = 2

        clients_map = np.array([
            [3, 0, 0, 0, 2],
            [2, 0, 1, 0, 0],
            [0, 2, 0, 0, 0],
            [1, 0, 2, 1, 1],
            [5, 5, 0, 0, 1],
            [1, 1, 1, 0, 0],
            [0, 0, 0, 1, 0]
        ])

        ind = (3, 2)

        start_gen = StartingSolutionGenerator.StartingSolutionGen(n_max,
                                                                  p_max,
                                                                  d_max,
                                                                  clients_map)

        expected = np.array([
            [3, 0, 0, 0, 2],
            [2, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [5, 0, 0, 0, 1],
            [1, 1, 0, 0, 0],
            [0, 0, 0, 1, 0]
        ])

        start_gen._StartingSolutionGen__make_mask_matrix()
        start_gen._StartingSolutionGen__reduce_temp_clients_map(ind)

        self.assertTrue(np.all(expected == start_gen._StartingSolutionGen__temp_clients_map))

    def test_generate(self):
        n_max = 4
        p_max = 8
        d_max = 2

        clients_map = np.array([
            [3, 0, 0, 0, 2],
            [0, 0, 1, 0, 0],
            [0, 2, 0, 0, 0],
            [0, 0, 0, 1, 5]
        ])

        start_gen = StartingSolutionGenerator.StartingSolutionGen(n_max,
                                                                  p_max,
                                                                  d_max,
                                                                  clients_map)

        expected = np.array([
            [1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0]
        ])

        got = start_gen.generate()

        self.assertTrue(np.all(expected == got))

    def test_generate_2(self):
        n_max = 5
        p_max = 10
        d_max = 2

        clients_map = np.array([
            [3, 0, 0, 0, 2],
            [0, 0, 1, 0, 0],
            [0, 2, 0, 0, 0],
            [1, 0, 0, 1, 5]
        ])

        start_gen = StartingSolutionGenerator.StartingSolutionGen(n_max,
                                                                  p_max,
                                                                  d_max,
                                                                  clients_map)

        expected = np.array([
            [1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0]
        ])

        got = start_gen.generate()

        self.assertTrue(np.all(expected == got))

    def test_generate_3(self):
        n_max = 5
        p_max = 10
        d_max = 2

        clients_map = np.array([
            [3, 0, 0, 0, 2],
            [9, 0, 1, 0, 0],
            [0, 2, 0, 0, 0],
            [1, 0, 0, 1, 5]
        ])

        start_gen = StartingSolutionGenerator.StartingSolutionGen(n_max,
                                                                  p_max,
                                                                  d_max,
                                                                  clients_map)

        expected = np.array([
            [0, 0, 1, 1, 1],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0]
        ])

        got = start_gen.generate()

        self.assertTrue(np.all(expected == got))

    def test_generate_raise_error(self):
        n_max = 5
        p_max = 10
        d_max = 2

        clients_map = np.array([
            [3, 0, 0, 0, 2],
            [9, 0, 1, 9, 0],
            [0, 2, 0, 0, 0],
            [1, 0, 9, 1, 5]
        ])

        start_gen = StartingSolutionGenerator.StartingSolutionGen(n_max,
                                                                  p_max,
                                                                  d_max,
                                                                  clients_map)

        self.assertRaises(RuntimeError, start_gen.generate)


if __name__ == '__main__':
    unittest.main()
