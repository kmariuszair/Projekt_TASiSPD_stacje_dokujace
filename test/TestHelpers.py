import unittest
import numpy as np
import os

import src.Helpers as Helpers


class TestHelpers(unittest.TestCase):

    def test_rand_docks_gen(self):
        allowed = np.load(str(os.path.dirname(__file__))[:-5] + '\\maps\\case1\\barriers.npy')

        frame = 3
        for _ in range(100):
            docks, _ = Helpers.generate_docking_stations_map(allowed, 50, frame)
            self.assertFalse(np.any(docks[frame:-frame, frame:-frame]))
            self.assertEqual(np.count_nonzero(docks), 50)
            self.assertFalse(np.any(docks[allowed>0]))



if __name__ == '__main__':
    unittest.main()
