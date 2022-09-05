import logging
import os
import random
import unittest
from pathlib import Path

from prime import next_prime
from tonellishanks import tonelli_shanks, legendre_symbol


_logger = logging.getLogger("tonellishanks")


def _resolve_base_path():
    base_path = Path(__file__).parent
    return (base_path / "../").resolve()


_logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(os.path.join(_resolve_base_path(), "tonellishanks.log"), mode="w")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(asctime)s %(levelname)7s]: %(message)s")
file_handler.setFormatter(formatter)

_logger.addHandler(file_handler)


class TonelliShanksTests(unittest.TestCase):

    def check_square(self, a: int, alleged_root_of_a: int, p: int):
        alleged_square = (alleged_root_of_a * alleged_root_of_a) % p
        self.assertEqual(a, alleged_square, msg="a = %d, p = %d" % (a, p))

    def simple_test(self, a: int, p: int, /, *, det: bool = True):
        _logger.info("========== Starting test [a = %d, p = %d] ==========", a, p)
        root = tonelli_shanks(a, p, deterministic=det)
        self.check_square(a, root, p)

    def test_1(self):
        self.simple_test(8, 17)

    def test_2(self):
        self.simple_test(9, 17)

    def test_3(self):
        self.simple_test(39, 41)

    def test_4(self):
        self.simple_test(13, 10000019)

    def interval_test(self, p_low: int, p_high: int, /, *, det: bool):

        assert p_low < p_high

        p = next_prime(p_low)

        while p < p_high:
            for __ in range(min(p, 0x100)):

                a = random.randrange(2, p)

                if legendre_symbol(a, p) == 1:
                    # a is a square modulo p
                    self.simple_test(a, p, det=det)

            p = next_prime(p)

    def interval_test_full(self, p_low: int, p_high: int, /):
        self.interval_test(p_low, p_high, det=True)
        self.interval_test(p_low, p_high, det=False)

    def test_until_1000(self):
        self.interval_test_full(3, 1000)

    def test_until_2000(self):
        self.interval_test_full(1000, 2000)

    def test_until_3000(self):
        self.interval_test_full(2000, 3000)

    def test_until_4000(self):
        self.interval_test_full(3000, 4000)

    def test_until_5000(self):
        self.interval_test_full(4000, 5000)

    def test_until_6000(self):
        self.interval_test_full(5000, 6000)

    def test_until_7000(self):
        self.interval_test_full(6000, 7000)

    def test_until_8000(self):
        self.interval_test_full(7000, 8000)

    def test_until_9000(self):
        self.interval_test_full(8000, 9000)

    def test_until_10000(self):
        self.interval_test_full(9000, 10000)

    def test_mersenne(self):
        self.simple_test(17, (1 << 19937) - 1)
