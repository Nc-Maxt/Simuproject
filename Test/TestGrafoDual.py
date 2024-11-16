import sys, os
import numpy as np
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from UniformTrees.dust import Dualgraph


class TestGrafoDual(unittest.TestCase):
    def setUp(self):
        self.d_1 = Dualgraph((10, 10))
        self.d_2 = Dualgraph((7, 19))

    def testShape(self):
        self.assertEqual(self.d_1.graph.shape, (10, 10))
        self.assertEqual(self.d_2.graph.shape, (7, 19))
        self.assertEqual(self.d_1.shape, (41, 41))
        self.assertEqual(self.d_2.shape, (29, 77))

    def testAppend(self):
        verts = np.array([[0, n] for n in range(41)])
        self.assertTrue((self.d_1.grid == 0).all())
        self.d_1.append(verts)
        self.assertTrue((self.d_1.grid[0, :] == 1).all())
        self.assertTrue((self.d_1.grid != 1).any())

    # def testReescalate(self):
    #     self.d_1.reescalategraph()
    #     self.assertTrue((self.d_1.graph.grid == 1).all())
    #     self.d_2.reescalategraph()
    #     self.assertTrue((self.d_2.graph.grid == 1).all())


if __name__ == "__main__":
    unittest.main()
