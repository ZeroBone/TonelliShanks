import random
import unittest

from prime import next_prime
from tonellishanks import tonelli_shanks, legendre_symbol


class TonelliShanksTests(unittest.TestCase):

    def check_square(self, a: int, alleged_root_of_a: int, p: int):
        alleged_square = (alleged_root_of_a * alleged_root_of_a) % p
        self.assertEqual(a, alleged_square)

    def simple_test(self, a: int, p: int):
        root = tonelli_shanks(a, p)
        self.check_square(a, root, p)

    def test_1(self):
        self.simple_test(8, 17)

    def test_2(self):
        self.simple_test(39, 41)

    def test_batch(self):

        p = 3

        for _ in range(100):

            for __ in range(min(p, 200)):

                a = random.randrange(2, p)

                if legendre_symbol(a, p) == 1:
                    # a is a square modulo p
                    print("Testing with a = %d, p = %d" % (a, p))
                    self.simple_test(a, p)

            p = next_prime(p)
