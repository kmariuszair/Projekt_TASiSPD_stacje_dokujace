import unittest
import numpy as np

import src.Solver


class TestSolver(unittest.TestCase):

    def test_dist_to_nearest_pl(self):
        pl_map = np.array([
            [0, 0, 1],
            [1, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])

        clients_map = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 6]
        ])

        clients_pos = np.where(clients_map == 6)
        clients_pos = (int(clients_pos[0]), int(clients_pos[1]))

        test_solver = src.Solver.Solver(n_max=1,
                                        p_max=1,
                                        d_max=4,
                                        r=1,
                                        min_time_in_tl=1,
                                        min_time_in_lt_tl=1,
                                        client_map=clients_map,
                                        time_lim=0,
                                        starting_solution=pl_map)

        expected_dist = 4

        self.assertTrue(expected_dist, test_solver._Solver__dist_to_nearest_pl(clients_pos, pl_map))

    def test_dist_to_nearest_pl_r(self):
            pl_map = np.array([
                [0, 0, 0],
                [0, 0, 0],
                [1, 0, 0],
                [0, 0, 1]
            ])

            clients_map = np.array([
                [0, 0, 6],
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]
            ])

            clients_pos = np.where(clients_map == 6)
            clients_pos = (int(clients_pos[0]), int(clients_pos[1]))

            test_solver = src.Solver.Solver(n_max=1,
                                            p_max=1,
                                            d_max=4,
                                            r=1,
                                            min_time_in_tl=1,
                                            min_time_in_lt_tl=1,
                                            client_map=clients_map,
                                            time_lim=0,
                                            starting_solution=pl_map)

            expected_dist = 4

            self.assertTrue(expected_dist, test_solver._Solver__dist_to_nearest_pl(clients_pos, pl_map))

    def test_stop_condition_iter_false(self):
        pl_map = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])

        clients_map = np.array([
            [0, 0, 6],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])

        test_solver = src.Solver.Solver(n_max=1,
                                        p_max=1,
                                        d_max=4,
                                        r=1,
                                        min_time_in_tl=10,

                                        min_time_in_lt_tl=1,
                                        iteration_lim=10,

                                        client_map=clients_map,
                                        starting_solution=pl_map)

        test_solver._Solver__curr_it = 9

        self.assertFalse(test_solver._Solver__stop_condition())

    def test_stop_condition_iter_true(self):
        pl_map = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])

        clients_map = np.array([
            [0, 0, 6],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])

        test_solver = src.Solver.Solver(n_max=1,
                                        p_max=1,
                                        d_max=4,
                                        r=1,
                                        min_time_in_tl=10,

                                        min_time_in_lt_tl=1,
                                        iteration_lim=10,

                                        client_map=clients_map,
                                        starting_solution=pl_map)

        test_solver._Solver__curr_it = 11

        self.assertTrue(test_solver._Solver__stop_condition())

    def test_stop_condition_time_false(self):
        pl_map = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])

        clients_map = np.array([
            [0, 0, 6],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])

        test_solver = src.Solver.Solver(n_max=1,
                                        p_max=1,
                                        d_max=4,
                                        r=1,
                                        min_time_in_tl=10,

                                        min_time_in_lt_tl=1,
                                        time_lim=10,

                                        client_map=clients_map,
                                        starting_solution=pl_map)

        test_solver._Solver__curr_it = 9

        self.assertFalse(test_solver._Solver__stop_condition())

    def test_stop_condition_time_true(self):
        pl_map = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])

        clients_map = np.array([
            [0, 0, 6],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])

        test_solver = src.Solver.Solver(n_max=1,
                                        p_max=1,
                                        d_max=4,
                                        r=1,
                                        min_time_in_tl=10,

                                        min_time_in_lt_tl=1,
                                        time_lim=10,

                                        client_map=clients_map,
                                        starting_solution=pl_map)

        test_solver._Solver__curr_it = 11

        self.assertFalse(test_solver._Solver__stop_condition())

    def test_is_in_tabu_false(self):
        pl_map = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])

        clients_map = np.array([
            [0, 0, 6],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])

        test_solver = src.Solver.Solver(n_max=5,
                                        p_max=1,
                                        d_max=4,
                                        r=1,
                                        min_time_in_tl=10,

                                        min_time_in_lt_tl=1,
                                        time_lim=10,

                                        client_map=clients_map,
                                        starting_solution=pl_map)

        fake_tabu_list = np.array([
            [0, 5, 1],
            [0, 2, 0],
            [0, 3, 0],
            [0, 0, 0]
        ])

        test_solver._Solver__tabu_list = fake_tabu_list

        x_new = np.array([
            [1, 0, 0],
            [1, 0, 1],
            [0, 0, 1],
            [0, 1, 0]
        ])

        self.assertFalse(test_solver._Solver__is_in_tabu_list(x_new)[0])

    def test_is_in_tabu_true(self):
        pl_map = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])

        clients_map = np.array([
            [0, 0, 6],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])

        test_solver = src.Solver.Solver(n_max=5,
                                        p_max=1,
                                        d_max=4,
                                        r=1,
                                        min_time_in_tl=10,

                                        min_time_in_lt_tl=1,
                                        time_lim=10,

                                        client_map=clients_map,
                                        starting_solution=pl_map)

        fake_tabu_list = np.array([
            [0, 5, 1],
            [0, 2, 0],
            [0, 3, 0],
            [0, 0, 0]
        ])

        test_solver._Solver__tabu_list = fake_tabu_list

        x_new = np.array([
            [1, 0, 0],
            [1, 0, 1],
            [0, 1, 1],
            [0, 0, 0]
        ])

        self.assertTrue(test_solver._Solver__is_in_tabu_list(x_new)[0])

    def test_is_in_tabu_true_two_in_tabu(self):
        # ten przypadek nie powinien się przydarzyć w przebiegu algorytmu przy przyjętym sąsiedztwie
        pl_map = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])

        clients_map = np.array([
            [0, 0, 6],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])

        test_solver = src.Solver.Solver(n_max=5,
                                        p_max=1,
                                        d_max=4,
                                        r=1,
                                        min_time_in_tl=10,

                                        min_time_in_lt_tl=1,
                                        time_lim=10,

                                        client_map=clients_map,
                                        starting_solution=pl_map)

        fake_tabu_list = np.array([
            [0, 5, 1],
            [0, 2, 0],
            [0, 3, 0],
            [0, 0, 0]
        ])

        test_solver._Solver__tabu_list = fake_tabu_list

        x_new = np.array([
            [1, 0, 0],
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0]
        ])

        self.assertTrue(test_solver._Solver__is_in_tabu_list(x_new)[0])

    def test_change_times_to_left_tl(self):
        pl_map = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])

        clients_map = np.array([
            [0, 0, 6],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])

        test_solver = src.Solver.Solver(n_max=5,
                                        p_max=1,
                                        d_max=4,
                                        r=1,
                                        min_time_in_tl=10,

                                        min_time_in_lt_tl=1,
                                        time_lim=10,

                                        client_map=clients_map,
                                        starting_solution=pl_map)

        fake_tabu_list = np.array([
            [0, 5, 1],
            [0, 2, 0],
            [0, 3, 0],
            [0, 0, 0]
        ])

        test_solver._Solver__tabu_list = fake_tabu_list
        test_solver._Solver__change_times_to_left_tl()

        modified_tabu_list = np.array([
            [0, 4, 0],
            [0, 1, 0],
            [0, 2, 0],
            [0, 0, 0]
        ])

        np.testing.assert_array_equal(test_solver._Solver__tabu_list, modified_tabu_list)

    def test_delete_given_move_from_tabu(self):
        pl_map = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])

        clients_map = np.array([
            [0, 0, 6],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])

        test_solver = src.Solver.Solver(n_max=5,
                                        p_max=1,
                                        d_max=4,
                                        r=1,
                                        min_time_in_tl=10,

                                        min_time_in_lt_tl=1,
                                        time_lim=10,

                                        client_map=clients_map,
                                        starting_solution=pl_map)

        fake_tabu_list = np.array([
            [0, 5, 1],
            [0, 2, 0],
            [0, 3, 0],
            [0, 0, 0]
        ])

        test_solver._Solver__tabu_list = fake_tabu_list
        test_solver._Solver__delete_given_move_from_tabu((0, 1))

        modified_tabu_list = np.array([
            [0, 0, 1],
            [0, 2, 0],
            [0, 3, 0],
            [0, 0, 0]
        ])

        np.testing.assert_array_equal(test_solver._Solver__tabu_list, modified_tabu_list)

    def test_add_move_to_tabu_list(self):
        pl_map = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])

        clients_map = np.array([
            [0, 0, 6],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])

        test_solver = src.Solver.Solver(n_max=5,
                                        p_max=1,
                                        d_max=4,
                                        r=1,
                                        min_time_in_tl=10,

                                        min_time_in_lt_tl=1,
                                        time_lim=10,

                                        client_map=clients_map,
                                        starting_solution=pl_map)

        fake_tabu_list = np.array([
            [0, 5, 1],
            [0, 2, 0],
            [0, 3, 0],
            [0, 0, 0]
        ])

        move = np.array([
            [0, 0, 0],
            [0, 0,-1],
            [1, 0, 0],
            [0, 0, 0]
        ])

        test_solver._Solver__tabu_list = fake_tabu_list
        test_solver._Solver__add_move_to_tabu_list(move)

        modified_tabu_list = np.array([
            [0, 5, 1],
            [0, 2, 0],
            [10,3, 0],
            [0, 0, 0]
        ])

        np.testing.assert_array_equal(test_solver._Solver__tabu_list, modified_tabu_list)

    def test_is_in_lt_tabu_false(self):
        pl_map = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])

        clients_map = np.array([
            [0, 0, 6],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])

        test_solver = src.Solver.Solver(n_max=5,
                                        p_max=1,
                                        d_max=4,
                                        r=1,
                                        min_time_in_tl=10,

                                        min_time_in_lt_tl=1,
                                        time_lim=10,

                                        client_map=clients_map,
                                        starting_solution=pl_map)

        fake_tabu_list = np.array([
            [0, 5, 1],
            [0, 2, 0],
            [0, 3, 0],
            [0, 0, 0]
        ])

        test_solver._Solver__long_term_tabu_list = fake_tabu_list

        x_new = np.array([
            [0, 1, 1],
            [0, 1, 1],
            [0, 1, 0],
            [0, 0, 0]
        ])

        is_in_long_tabu, _ = test_solver._Solver__is_in_long_term_tabu_list(x_new)
        self.assertFalse(is_in_long_tabu)

    def test_is_in_long_term_tabu_true(self):
        pl_map = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])

        clients_map = np.array([
            [0, 0, 6],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])

        test_solver = src.Solver.Solver(n_max=5,
                                        p_max=1,
                                        d_max=4,
                                        r=1,
                                        min_time_in_tl=10,

                                        min_time_in_lt_tl=1,
                                        time_lim=10,

                                        client_map=clients_map,
                                        starting_solution=pl_map)

        fake_tabu_list = np.array([
            [0, 5, 1],
            [0, 2, 0],
            [0, 3, 0],
            [0, 0, 0]
        ])

        test_solver._Solver__long_term_tabu_list = fake_tabu_list

        x_new = np.array([
            [0, 1, 1],
            [1, 0, 1],
            [0, 1, 0],
            [0, 0, 0]
        ])

        is_in_long_tabu, _ = test_solver._Solver__is_in_long_term_tabu_list(x_new)
        self.assertTrue(is_in_long_tabu)

    def test_is_in_long_term_tabu_true_two_in_tabu(self):
        # ten przypadek nie powinien się przydarzyć w przebiegu algorytmu przy przyjętym sąsiedztwie
        pl_map = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])

        clients_map = np.array([
            [0, 0, 6],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])

        test_solver = src.Solver.Solver(n_max=5,
                                        p_max=1,
                                        d_max=4,
                                        r=1,
                                        min_time_in_tl=10,

                                        min_time_in_lt_tl=1,
                                        time_lim=10,

                                        client_map=clients_map,
                                        starting_solution=pl_map)

        fake_tabu_list = np.array([
            [0, 5, 1],
            [0, 2, 0],
            [0, 3, 0],
            [0, 0, 0]
        ])

        test_solver._Solver__long_term_tabu_list = fake_tabu_list

        x_new = np.array([
            [1, 0, 0],
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0]
        ])

        is_in_long_tabu, _ = test_solver._Solver__is_in_long_term_tabu_list(x_new)
        self.assertTrue(is_in_long_tabu)

    def test_change_times_to_left_long_term_tl(self):
        pl_map = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])

        clients_map = np.array([
            [0, 0, 6],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])

        test_solver = src.Solver.Solver(n_max=5,
                                        p_max=1,
                                        d_max=4,
                                        r=1,
                                        min_time_in_tl=10,

                                        min_time_in_lt_tl=1,
                                        time_lim=10,

                                        client_map=clients_map,
                                        starting_solution=pl_map)

        fake_tabu_list = np.array([
            [0, 5, 1],
            [0, 2, 0],
            [0, 3, 0],
            [0, 0, 0]
        ])

        test_solver._Solver__long_term_tabu_list = fake_tabu_list
        test_solver._Solver__change_times_to_left_lt_tl()

        modified_tabu_list = np.array([
            [0, 4, 0],
            [0, 1, 0],
            [0, 2, 0],
            [0, 0, 0]
        ])

        np.testing.assert_array_equal(test_solver._Solver__long_term_tabu_list, modified_tabu_list)

    def test_delete_given_move_from_long_term_tabu(self):
        pl_map = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])

        clients_map = np.array([
            [0, 0, 6],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])

        test_solver = src.Solver.Solver(n_max=5,
                                        p_max=1,
                                        d_max=4,
                                        r=1,
                                        min_time_in_tl=10,

                                        min_time_in_lt_tl=1,
                                        time_lim=10,

                                        client_map=clients_map,
                                        starting_solution=pl_map)

        fake_tabu_list = np.array([
            [0, 5, 1],
            [0, 2, 0],
            [0, 3, 0],
            [0, 0, 0]
        ])

        test_solver._Solver__long_term_tabu_list = fake_tabu_list
        test_solver._Solver__delete_given_move_from_long_term_tabu((0, 1))

        modified_tabu_list = np.array([
            [0, 0, 1],
            [0, 2, 0],
            [0, 3, 0],
            [0, 0, 0]
        ])

        np.testing.assert_array_equal(test_solver._Solver__long_term_tabu_list, modified_tabu_list)

    def test_add_move_to_long_term_tabu_list(self):
        pl_map = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 1]
        ])

        clients_map = np.array([
            [0, 0, 6],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])

        test_solver = src.Solver.Solver(n_max=5,
                                        p_max=1,
                                        d_max=4,
                                        r=1,
                                        min_time_in_tl=10,

                                        min_time_in_lt_tl=10,
                                        time_lim=10,

                                        client_map=clients_map,
                                        starting_solution=pl_map)

        fake_tabu_list = np.array([
            [0, 5, 1],
            [0, 2, 0],
            [0, 3, 0],
            [0, 0, 0]
        ])

        move = np.array([
            [0, 0, 0],
            [0, 0,-1],
            [1, 0, 0],
            [0, 0, 0]
        ])

        test_solver._Solver__long_term_tabu_list = fake_tabu_list
        test_solver._Solver__add_move_to_long_term_tabu_list(move)

        modified_tabu_list = np.array([
            [0, 5, 1],
            [0, 2,10],
            [0 ,3, 0],
            [0, 0, 0]
        ])

        np.testing.assert_array_equal(test_solver._Solver__long_term_tabu_list, modified_tabu_list)


if __name__ == '__main__':
    unittest.main()
