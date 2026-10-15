import unittest
from shop import apply_discount, parse_price, total


class ShopTests(unittest.TestCase):
    def test_parse_simple(self):
        self.assertEqual(parse_price("$10.50"), 10.5)

    def test_discount(self):
        self.assertAlmostEqual(apply_discount(200, 25), 150)

    def test_total(self):
        self.assertEqual(total([1, 2, 3]), 6)


if __name__ == "__main__":
    unittest.main()
