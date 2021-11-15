import unittest
import numpy as np
from multibody2D.physics import *
from multibody2D.util import *


class DYMUTestCase(unittest.TestCase):
    # TODO : testing
    def test_vector(self):
        obj = vector([1, 2, 3], 'v', name="v1")
        self.assert_(obj.is_vertical)
        self.assertFalse(obj.is_horizontal)

    def test_position_P_R0(self):
        Qs = np.array([[1, 1, np.pi/2]]).T
        GP_RS = np.array([[1, 0]]).T
        position_P_R0(Qs, GP_RS)

    def test_vitesse_P_R0(self):
        Qs = np.array([[1, 1, np.pi / 4]]).T
        dQs = np.array([[1, 0, 1]]).T
        GP_RS = np.array([[1, 0]]).T
        vitesse_P_R0(Qs, dQs, GP_RS)

    def test_acceleration_P_R0(self):
        Qs = np.array([[1, 1, np.pi / 4]]).T
        dQs = np.array([[1, 0, 1]]).T
        d2Qs = np.array([[0, 0, 0]]).T
        GP_RS = np.array([[1, 0]]).T
        acceleration_P_R0(Qs, dQs, d2Qs, GP_RS)

    def test_force_ressort_amortisseur(self):
        # Ressort
        L0 = 0
        k = 1e3
        c = 0

        Qs1 = np.array([[1, 1, np.pi / 4]]).T
        dQs1 = np.array([[1, 0, 1]]).T
        d2Qs1 = np.array([[0, 0, 0]]).T
        GP_RS1 = np.array([[1, 0]]).T
        Qs2 = np.array([[4, 4, np.pi / 4]]).T
        dQs2 = np.array([[1, 0, 1]]).T
        d2Qs2 = np.array([[0, 0, 0]]).T
        GP_RS2 = np.array([[-1, 0]]).T
        force_ressort_amortisseur(k, c, L0, Qs1, dQs1, GP_RS1, Qs2, dQs2, GP_RS2)


if __name__ == '__main__':
    unittest.main()
