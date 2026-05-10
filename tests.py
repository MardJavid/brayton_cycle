import unittest
import math
import funcs

class TestGetStateVariables(unittest.TestCase):

    def setUp(self):
        self.P1 = 100
        self.T1 = 300
        self.T3 = 1400
        self.rp = 8
        self.cp = 1.005
        self.gamma = 1.4

        self.result = funcs.getStateVariables(
            self.P1,
            self.T1,
            self.T3,
            self.rp,
            self.cp,
            self.gamma
        )

    def testReturnsList(self):
        self.assertIsInstance(self.result, list)

    def testReturnsFourPoints(self):
        self.assertEqual(len(self.result), 4)

    def testEachStateIsTuple(self):
        for state in self.result:
            self.assertIsInstance(state, tuple)

    def testEachTupleHasThreeValues(self):
        for state in self.result:
            self.assertEqual(len(state), 3)

    def testAllValuesAreNumeric(self):
        for state in self.result:
            for value in state:
                self.assertIsInstance(value, (int, float))

    def testP2(self):
        self.assertEqual(self.result[1][0], self.P1 * self.rp)

    def testP3(self):
        self.assertEqual(self.result[2][0], self.result[1][0])

    def testP4(self):
        self.assertEqual(self.result[3][0], self.P1)

    def testAllPressuresArePositive(self):
        for state in self.result:
            self.assertGreater(state[0], 0)

    # -------------------------
    # Temperature Logic
    # -------------------------

    def testT2(self):
        expected = self.T1 * (
            self.rp ** ((self.gamma - 1) / self.gamma)
        )

        self.assertAlmostEqual(
            self.result[1][2],
            expected,
            places=6
        )

    def testT4(self):
        expected = self.T3 / (
            self.rp ** ((self.gamma - 1) / self.gamma)
        )

        self.assertAlmostEqual(
            self.result[3][2],
            expected,
            places=6
        )

    def testT3GreaterThanT4(self):
        self.assertGreater(
            self.result[2][2],
            self.result[3][2]
        )

    def testAllTemperaturesArePositive(self):
        for state in self.result:
            self.assertGreater(state[2], 0)

    def testTemperatureRatio(self):
        t_ratio = self.result[1][2] / self.result[0][2]

        expected = self.rp ** (
            (self.gamma - 1) / self.gamma
        )

        self.assertAlmostEqual(t_ratio, expected, places=6)

    def testRpOneKeepsTemperaturesSame(self):
        result = funcs.getStateVariables(
            100, 300, 1400, 1, 1.005, 1.4
        )

        self.assertEqual(result[1][2], 300)
        self.assertEqual(result[3][2], 1400)

    # -------------------------
    # Specific Volume Logic
    # -------------------------

    def testSpecificVolumeFormula(self):
        R = ((self.gamma - 1) * self.cp) / self.gamma

        expected = R * self.T1 / self.P1

        self.assertAlmostEqual(
            self.result[0][1],
            expected,
            places=6
        )

    def testAllSpecificVolumes(self):
        for state in self.result:
            self.assertGreater(state[1], 0)

    def testCompressionDecreasesVolume(self):
        self.assertLess(
            self.result[1][1],
            self.result[0][1]
        )

    def testV2LessThanV3(self):
        self.assertLess(
            self.result[1][1],
            self.result[2][1]
        )

    # -------------------------
    # Extreme / Edge Cases
    # -------------------------

    def testHighPressureRatio(self):
        result = funcs.getStateVariables(
            100, 300, 1400, 50, 1.005, 1.4
        )

        self.assertGreater(result[1][2], 800)

    def testLowGamma(self):
        result = funcs.getStateVariables(
            100, 300, 1400, 8, 1.005, 1.01
        )

        self.assertEqual(len(result), 4)

    def testFloatInputs(self):
        result = funcs.getStateVariables(
            100.5, 300.2, 1400.8, 8.1, 1.005, 1.4
        )

        self.assertIsInstance(result, list)


# ==========================================================
# getWork TESTS
# ==========================================================

class TestGetWork(unittest.TestCase):

    def setUp(self):
        self.result = funcs.getWork(
            1,
            1.005,
            300,
            500,
            1400,
            900
        )

    # -------------------------
    # Structure / Types
    # -------------------------

    def testReturnsTuple(self):
        self.assertIsInstance(self.result, tuple)

    def testReturnsThreeValues(self):
        self.assertEqual(len(self.result), 3)

    def testAllOutputsNumeric(self):
        for value in self.result:
            self.assertIsInstance(value, (int, float))

    # -------------------------
    # Arithmetic
    # -------------------------

    def testCompressorWorkFormula(self):
        result = funcs.getWork(
            2, 1, 300, 500, 1400, 900
        )

        self.assertEqual(result[0], 400)

    def testTurbineWorkFormula(self):
        result = funcs.getWork(
            2, 1, 300, 500, 1400, 900
        )

        self.assertEqual(result[1], 1000)

    def testNetWorkFormula(self):
        result = funcs.getWork(
            2, 1, 300, 500, 1400, 900
        )

        self.assertEqual(result[2], 600)

    def testNetWorkEqualsDifference(self):
        self.assertEqual(
            self.result[2],
            self.result[1] - self.result[0]
        )

    # -------------------------
    # Signs / Positivity
    # -------------------------

    def testCompressorWorkPositive(self):
        self.assertGreater(self.result[0], 0)

    def testTurbineWorkPositive(self):
        self.assertGreater(self.result[1], 0)

    # -------------------------
    # Edge Cases
    # -------------------------

    def testZeroMass(self):
        self.assertRaises(ValueError, funcs.getWork, 0, 1.005, 300, 500, 1400, 900)

    def testZeroCp(self):
        self.assertRaises(ValueError, funcs.getWork, 1, 0, 300, 500, 1400, 900)

    def testNegativeMass(self):
        self.assertRaises(ValueError, funcs.getWork, -1, 1.005, 300, 500, 1400, 900)

    def testNegativeCp(self):
        self.assertRaises(ValueError, funcs.getWork, 1, -1.005, 300, 500, 1400, 900)

    def testEqualTemperature(self):
        self.assertRaises(ValueError, funcs.getWork, 1, 1.005, 300, 300, 1400, 1400)

    # -------------------------
    # Float / Precision
    # -------------------------

    def testFractionalInputs(self):
        result = funcs.getWork(
            1.5, 1.005, 310, 480, 1350, 850
        )

        self.assertIsInstance(result[0], float)

    def testLargeValues(self):
        result = funcs.getWork(
            10000, 1.005, 300, 500, 2000, 400
        )

        self.assertGreater(result[1], 10000000)

    def testSmallValues(self):
        result = funcs.getWork(
            0.001, 0.001, 300, 301, 302, 301
        )

        self.assertGreaterEqual(result[0], 0)


# ==========================================================
# getHeat TESTS
# ==========================================================

class TestGetHeat(unittest.TestCase):

    def setUp(self):
        self.result = funcs.getHeat(
            1,
            1.005,
            300,
            500,
            1400,
            900,
            201,
            502.5,
            301.5
        )

    # -------------------------
    # Structure / Types
    # -------------------------

    def testReturnsTuple(self):
        self.assertIsInstance(self.result, tuple)

    def testReturnsFourValues(self):
        self.assertEqual(len(self.result), 4)

    def testAllValuesNumerics(self):
        for value in self.result:
            self.assertIsInstance(value, (int, float))

    # -------------------------
    # Arithmetic
    # -------------------------

    def testQinFormula(self):
        result = funcs.getHeat(
            2, 1, 300, 500,
            1400, 900,
            400, 1000, 600
        )

        self.assertEqual(result[0], 1800)

    def testQoutFormula(self):
        result = funcs.getHeat(
            2, 1, 300, 500,
            1400, 900,
            400, 1000, 600
        )

        self.assertEqual(result[1], 1200)

    def testEfficiencyFormula(self):
        result = funcs.getHeat(
            2, 1, 300, 500,
            1400, 900,
            400, 1000, 600
        )

        self.assertAlmostEqual(
            result[2],
            600 / 1800
        )

    def testBwrFormula(self):
        result = funcs.getHeat(
            2, 1, 300, 500,
            1400, 900,
            400, 1000, 600
        )

        self.assertAlmostEqual(result[3], 0.4)

    # -------------------------
    # Logic
    # -------------------------

    def testQinPositive(self):
        self.assertGreater(self.result[0], 0)

    def testQoutPositive(self):
        self.assertGreater(self.result[1], 0)

    def testEfficiencyPositive(self):
        self.assertGreater(self.result[2], 0)

    def testEfficiencyLessThanOne(self):
        self.assertLess(self.result[2], 1)

    def testBwrLessThanOne(self):
        self.assertLess(self.result[3], 1)

    def testQinGreaterThanQout(self):
        self.assertGreater(
            self.result[0],
            self.result[1]
        )

    # -------------------------
    # Edge Cases
    # -------------------------

    def testZeroMass(self):
        self.assertRaises(ValueError, funcs.getHeat, 
            0, 1.005, 300, 500,
            1400, 900,
            201, 502.5, 301.5)

    def testZeroCp(self):
        self.assertRaises(ValueError, funcs.getHeat,  
            1, 0, 300, 500,
            1400, 900,
            201, 502.5, 301.5)

    def testNegativeMass(self):
        self.assertRaises(ValueError, funcs.getHeat, 
            -1, 1.005, 300, 500,
            1400, 900,
            201, 502.5, 301.5)

    def testNegativeCp(self):
        self.assertRaises(ValueError, funcs.getHeat, 
            1, -1.005, 300, 500,
            1400, 900,
            201, 502.5, 301.5)

    def testHighBackWorkRatio(self):
        self.assertRaises(ValueError, funcs.getHeat, 
            1, 1,
            300, 900,
            1400, 1000,
            600, 400, -200)

    # -------------------------
    # Float / Precision
    # -------------------------

    def testFractionalInputs(self):
        result = funcs.getHeat(
            1.5, 1.005,
            310, 480,
            1350, 850,
            256.275,
            753.75,
            497.475
        )

        self.assertIsInstance(result[2], float)

    def testLargeValues(self):
        result = funcs.getHeat(
            10000, 1.005,
            300, 500,
            3000, 1200,
            2010000,
            18090000,
            16080000
        )

        self.assertGreater(result[0], 10000000)

    def testSmallValues(self):
        result = funcs.getHeat(
            0.001, 0.001,
            300, 301,
            302, 301.5,
            0.1, 0.2, 0.1
        )

        self.assertGreaterEqual(result[0], 0)


if __name__ == "__main__":
    unittest.main()