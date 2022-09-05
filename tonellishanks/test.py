import random
import unittest

from prime import next_prime
from tonellishanks import tonelli_shanks, legendre_symbol


class TonelliShanksTests(unittest.TestCase):

    def check_square(self, a: int, alleged_root_of_a: int, p: int):
        alleged_square = (alleged_root_of_a * alleged_root_of_a) % p
        self.assertEqual(a, alleged_square, msg="a = %d, p = %d" % (a, p))

    def simple_test(self, a: int, p: int, /, *, det: bool = True):
        root = tonelli_shanks(a, p, deterministic=det)
        self.check_square(a, root, p)

    def test_1(self):
        self.simple_test(8, 17)

    def test_2(self):
        self.simple_test(39, 41)

    def batch_test(self, /, *, det: bool):

        p = 3

        for _ in range(10000):
            for __ in range(min(p, 350)):

                a = random.randrange(2, p)

                if legendre_symbol(a, p) == 1:
                    # a is a square modulo p
                    self.simple_test(a, p, det=det)

            p = next_prime(p)

    def test_batch_det(self):
        self.batch_test(det=True)

    def test_batch_randomized(self):
        self.batch_test(det=False)
