import unittest
import numpy as np
import Planner as pl

class TestPlanner(unittest.TestCase):
    def test_build_path(self):
        expected_planned_path = np.array([[ 0, 0, 0],[10, 0, 0],[20, 0,  0],[30, 0, 0],[40, 0, 0],
        [40, 10, 0],[40, 20, 0],[40, 30, 0],[40, 40, 0],
        [40, 40, 10],[40, 40, 20],[40, 40, 30],[40, 40, 40]])
        expected_planned_final_points = np.array([[ 0,  0,  0],[40, 0, 0],[40, 40, 0,],[40, 40, 40]])
        expected_planned_orientation =  np.array([[0.57735027, 0.57735027, 0.57735027],[0.57735027, 0.57735027, 0.57735027],
        [0.57735027, 0.57735027, 0.57735027],[0.57735027, 0.57735027, 0.57735027],[0.57735027, 0.57735027, 0.57735027],
        [0, 1, 0],[0, 1, 0],[0, 1, 0],[0, 1, 0],[0, 0, 1],[0, 0, 1],[0, 0, 1],[0, 0, 1]])
        expected_rotArray = np.array([[[1, 0, 0],[0, 1, 0],[0, 0, 1]],
        [[1, -0.3660254, 0],[ 0.78867513, 1, 0.78867513],[0, -0.3660254, 1]],
        [[1, 0, 0], [0, 1, 0],[0, 2, 1]]])
        initial_path = np.array([[0, 0, 0],[40, 0, 0],[40, 40, 0],[40, 40, 40]])
        disc = 10
        xLocal = np.array([1, 1, 1])
        planned_path, planned_final_points, planned_orientation, rotArray = pl.build(initial_path, disc, xLocal)

        self.assertTrue(np.allclose(expected_planned_path, planned_path))
        self.assertTrue(np.allclose(expected_planned_final_points, planned_final_points))
        self.assertTrue(np.allclose(expected_planned_orientation, planned_orientation))
        self.assertTrue(np.allclose(expected_rotArray, rotArray))

    def test_next_position(self):
        expected_position1 = np.array([20, 0, 0])
        position1 = pl.nextPosition(np.array([10, 0, 0]), 10, np.array([1, 0, 0]))
        expected_position2 = np.array([40, 20, 0])
        position2 = pl.nextPosition(np.array([40, 10, 0]), 10, np.array([0, 1, 0]))
        expected_position3 = [40, 40, 40]
        position3 = pl.nextPosition(np.array([40, 40, 30]), 10, np.array([0, 0, 1]))
        
        self.assertTrue(np.allclose(expected_position1, position1))
        self.assertTrue(np.allclose(expected_position2, position2))
        self.assertTrue(np.allclose(expected_position3, position3))
        self.assertFalse(np.allclose(expected_position1, position2))
        self.assertFalse(np.allclose(expected_position2, position3))
        self.assertFalse(np.allclose(expected_position3, position1))

    def test_rotation_matrix(self):
        expected_rot_matrix1 = np.array([[1, 0, 0],[0, 1, 0],[0, 0, 1]])
        expected_rot_matrix2 = np.array([[1, -0.3660254, 0],[0.78867513, 1, 0.78867513],[0, -0.3660254, 1]])
        expected_rot_matrix3 = np.array([[1, 0, 0],[0, 1, 0],[0, 2, 1]])
        vec11 = np.array([1, 1, 1])
        vec12 = np.array([1, 1, 1])
        vec21 = np.array([0.57735027, 0.57735027, 0.57735027])
        vec22 = np.array([0, 1, 0])
        vec31 = np.array([0, 1, 0])
        vec32 = np.array([0, 0, 1])
        rot_matrix1 = pl.rotation_matrix(vec11, vec12)
        rot_matrix2 = pl.rotation_matrix(vec21, vec22)
        rot_matrix3 = pl.rotation_matrix(vec31, vec32)
        self.assertTrue(np.allclose(expected_rot_matrix1, rot_matrix1))
        self.assertTrue(np.allclose(expected_rot_matrix2, rot_matrix2))
        self.assertTrue(np.allclose(expected_rot_matrix3, rot_matrix3))
        self.assertFalse(np.allclose(expected_rot_matrix1, rot_matrix2))
        self.assertFalse(np.allclose(expected_rot_matrix2, rot_matrix3))
        self.assertFalse(np.allclose(expected_rot_matrix3, rot_matrix1))

    def test_unit_vector(self):
        expected_unit_vector1 = np.array([0.29138576, 0.87415728, 0.38851434])
        unit_vector1 = pl.unit_vector(np.array([[3, 9, 4]]))
        expected_unit_vector2 = np.array([1, 0, 0])
        unit_vector2 = pl.unit_vector(np.array([[1, 0, 0]]))
        expected_unit_vector3 = np.array([-1, 0, 0])
        unit_vector3 = pl.unit_vector(np.array([[-5, 0, 0]]))
        self.assertTrue(np.allclose(expected_unit_vector1, unit_vector1))
        self.assertTrue(np.allclose(expected_unit_vector2, unit_vector2))
        self.assertTrue(np.allclose(expected_unit_vector3, unit_vector3))