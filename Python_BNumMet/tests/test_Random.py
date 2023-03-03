from BNumMet import Random
from unittest import TestCase


class test_Random(TestCase):
    test_label = "Random Number Generator"

    def test_lehmers_start(self):
        Random.clear_lehmers_vars()
        # Tests that Lehmers Variables are initialized to None
        self.assertEqual(Random.lehmers_vars["a"], None)
        self.assertEqual(Random.lehmers_vars["c"], None)
        self.assertEqual(Random.lehmers_vars["m"], None)
        self.assertEqual(Random.lehmers_vars["x"], None)

    def test_lehmers_init(self):
        # Tests that Lehmers Variables are initialized correctly
        Random.clear_lehmers_vars()
        Random.lehmers_init(2, 3, 5, 1)
        self.assertEqual(Random.lehmers_vars["a"], 2)
        self.assertEqual(Random.lehmers_vars["c"], 3)
        self.assertEqual(Random.lehmers_vars["m"], 5)
        self.assertEqual(Random.lehmers_vars["x"], 1)
        Random.clear_lehmers_vars()

    def test_lehmers_default(self):
        # Tests that Lehmers Variables are initialized to default values
        Random.clear_lehmers_vars()
        Random.lehmers_rand()
        self.assertEqual(Random.lehmers_vars["a"], 7**5)
        self.assertEqual(Random.lehmers_vars["c"], 0)
        self.assertEqual(Random.lehmers_vars["m"], 2**31 - 1)
        Random.clear_lehmers_vars()

    def test_lehmers_initFixed(self):
        # Tests that Lehmers Variables are initialized correctly
        Random.clear_lehmers_vars()
        Random.lehmers_rand(2, 3, 5, 1)
        self.assertEqual(Random.lehmers_vars["a"], 2)
        self.assertEqual(Random.lehmers_vars["c"], 3)
        self.assertEqual(Random.lehmers_vars["m"], 5)
        Random.clear_lehmers_vars()

    def test_lehmers_rand_formula(self):
        arr = [1]
        maxIter = 100
        for i in range(maxIter):
            aux = Random.lehmers_rand(a=2**16 + 3, m=2**31, c=0, x=arr[-1])
            if len(arr) >= 3:
                lehmerFormula = (
                    6 * arr[-1] - 9 * arr[-2]
                ) % 1  # Test Xn = (6Xn-1 - 9Xn-2)
                self.assertEqual(lehmerFormula, aux)
            arr.append(aux)

    def test_marsaglia_start(self):
        Random.clear_marsaglia_vars()
        # Tests that Marsaglia Variables are initialized to None
        self.assertEqual(Random.marsaglia_vars["base"], None)
        self.assertEqual(Random.marsaglia_vars["lag_r"], None)
        self.assertEqual(Random.marsaglia_vars["lag_s"], None)
        self.assertEqual(Random.marsaglia_vars["carry"], None)
        self.assertEqual(Random.marsaglia_vars["args"], None)

    def test_marsaglia_init(self):
        # Tests that Marsaglia Variables are initialized correctly
        Random.clear_marsaglia_vars()
        Random.marsaglia_init(2, 2, 1, 1, seed_tuple=(1, 2))
        self.assertEqual(Random.marsaglia_vars["base"], 2)
        self.assertEqual(Random.marsaglia_vars["lag_r"], 2)
        self.assertEqual(Random.marsaglia_vars["lag_s"], 1)
        self.assertEqual(Random.marsaglia_vars["carry"], 1)
        self.assertEqual(Random.marsaglia_vars["args"], [1, 2])

        Random.clear_marsaglia_vars()
        # Exception: seedTuple must be a tuple of length 2
        with self.assertRaises(Exception):
            Random.marsaglia_init(2, 3, 5, 1, seed_tuple=1)
        with self.assertRaises(Exception):
            Random.marsaglia_init(2, 3, 5, 1, seed_tuple=(1, 2, 3))

        # Exception: lag_r and lag_s must be greater than 0
        with self.assertRaises(Exception):
            Random.marsaglia_init(2, 0, 5, 1)
        with self.assertRaises(Exception):
            Random.marsaglia_init(2, 3, 0, 1)

        # Exception: lag_r must be greater than or equal to lag_s
        with self.assertRaises(Exception):
            Random.marsaglia_init(2, 3, 2, 1)

        # Exception: carry must be 0 or 1
        with self.assertRaises(Exception):
            Random.marsaglia_init(2, 3, 5, 2)

        # Exception: base must be greater than 0
        with self.assertRaises(Exception):
            Random.marsaglia_init(0, 3, 5, 1)

    def test_marsaglia_default(self):
        # Tests that Marsaglia Variables are initialized to default values
        Random.clear_marsaglia_vars()
        Random.marsaglia_rand()
        self.assertEqual(Random.marsaglia_vars["base"], 2**31 - 1)
        self.assertEqual(Random.marsaglia_vars["lag_r"], 19)
        self.assertEqual(Random.marsaglia_vars["lag_s"], 7)
        self.assertEqual(Random.marsaglia_vars["carry"], 1)
        Random.clear_marsaglia_vars()

    def test_marsaglia_initFixed(self):
        # Tests that Marsaglia Variables are initialized correctly
        Random.clear_marsaglia_vars()
        Random.marsaglia_rand(2, 2, 1, 1, seed_tuple=(1, 2))
        self.assertEqual(Random.marsaglia_vars["base"], 2)
        self.assertEqual(Random.marsaglia_vars["lag_r"], 2)
        self.assertEqual(Random.marsaglia_vars["lag_s"], 1)
        self.assertEqual(Random.marsaglia_vars["carry"], 1)
        self.assertEqual(Random.marsaglia_vars["args"][0], 2)
        Random.clear_marsaglia_vars()

    def test_marsaglia_rand_formula(self):
        testArr = [
            0,
            1,
            9,
            1,
            7,
            4,
            2,
            2,
            0,
            2,
            8,
            3,
            4,
            9,
        ]  # According to Bibliography
        resArr = [0, 1]
        Random.clear_marsaglia_vars()
        for _ in range(len(testArr) - 2):
            resArr.append(
                Random.marsaglia_rand(
                    base=10, lag_r=2, lag_s=1, carry=0, seed_tuple=(0, 1)
                )
            )
            self.assertEqual(testArr[: len(resArr)], resArr)
