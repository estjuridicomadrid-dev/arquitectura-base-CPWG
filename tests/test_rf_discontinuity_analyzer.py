import math
import unittest

from rf_discontinuity_analyzer import analyze_transition, estimate_impedance


class EstimateImpedanceTests(unittest.TestCase):
    def test_valid_geometry_has_positive_impedance(self):
        impedance = estimate_impedance(0.3, 0.2, 4.2)

        self.assertGreater(impedance, 0.0)

    def test_rejects_invalid_geometry(self):
        with self.assertRaises(ValueError):
            estimate_impedance(0.0, 0.2, 4.2)

        with self.assertRaises(ValueError):
            estimate_impedance(0.3, 0.2, 0.5)


class AnalyzeTransitionTests(unittest.TestCase):
    def test_matching_geometries_have_no_reflection(self):
        result = analyze_transition(0.3, 0.2, 0.3, 0.2, 4.2)

        self.assertAlmostEqual(result.reflection_coefficient, 0.0)
        self.assertTrue(math.isinf(result.return_loss_db))
        self.assertAlmostEqual(result.vswr, 1.0)

    def test_geometry_step_has_finite_reflection(self):
        result = analyze_transition(0.3, 0.2, 0.2, 0.2, 4.2)

        self.assertGreater(abs(result.reflection_coefficient), 0.0)
        self.assertLess(abs(result.reflection_coefficient), 1.0)
        self.assertGreater(result.return_loss_db, 0.0)
        self.assertGreater(result.vswr, 1.0)


if __name__ == "__main__":
    unittest.main()
