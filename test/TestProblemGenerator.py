import unittest
import numpy as np

import src.ProblemGenerator


class TestProblemGenerator(unittest.TestCase):

    def test_random_problem_gen_size(self):

        map_shape = (20, 30)
        clients_number = 1234
        max_clients_number_in_cell = 10

        random_gen = src.ProblemGenerator.RandomProblemGen(map_shape=map_shape,
                                                           clients_number=clients_number,
                                                           max_clients_number_in_cell=max_clients_number_in_cell)

        generated_problem = random_gen.generate_problem()

        self.assertTupleEqual(map_shape, generated_problem.shape)

    def test_random_problem_gen_max_clients_in_cell(self):

        map_shape = (20, 30)
        clients_number = 1234
        max_clients_number_in_cell = 10

        random_gen = src.ProblemGenerator.RandomProblemGen(map_shape=map_shape,
                                                           clients_number=clients_number,
                                                           max_clients_number_in_cell=max_clients_number_in_cell)

        generated_problem = random_gen.generate_problem()
        more_than_max = np.count_nonzero(generated_problem > max_clients_number_in_cell)

        self.assertEqual(0, more_than_max)

    def test_random_problem_gen_min_clients_in_cell(self):

        map_shape = (20, 30)
        clients_number = 1234
        max_clients_number_in_cell = 10

        random_gen = src.ProblemGenerator.RandomProblemGen(map_shape=map_shape,
                                                           clients_number=clients_number,
                                                           max_clients_number_in_cell=max_clients_number_in_cell)

        generated_problem = random_gen.generate_problem()
        less_than_zero = np.count_nonzero(generated_problem < 0)

        self.assertEqual(0, less_than_zero)

    def test_random_problem_gen_sum_clients_on_map(self):

        map_shape = (20, 30)
        clients_number = 1234
        max_clients_number_in_cell = 10

        random_gen = src.ProblemGenerator.RandomProblemGen(map_shape=map_shape,
                                                           clients_number=clients_number,
                                                           max_clients_number_in_cell=max_clients_number_in_cell)

        generated_problem = random_gen.generate_problem()
        generated_clients_no = np.sum(generated_problem)

        self.assertEqual(clients_number, generated_clients_no)


if __name__ == '__main__':
    unittest.main()
