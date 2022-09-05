import random
import logging
import sys

from euklidian import inverse_modulo
from powmod import power_modulo
from prime import is_prime

_logger = logging.getLogger("tonellishanks")


def legendre_symbol(a: int, p: int, /) -> int:

    assert p % 2 != 0

    return power_modulo(a, (p - 1) >> 1, p)


def _choose_b(p: int, /, *, det=True) -> int:

    assert p % 2 != 0

    b = 2
    _attempts = 1

    if det:
        while legendre_symbol(b, p) == 1:
            b += 1
            _attempts += 1
    else:
        while legendre_symbol(b, p) == 1:
            b = random.randrange(2, p)
            _attempts += 1

    assert b < p
    assert legendre_symbol(b, p) == p - 1

    _logger.info("Found b = %d after %d attempts", b, _attempts)

    return b


def _tonelli_shanks_recursive(a: int, k: int, p: int, b: int, b_inverse: int, /):
    """
    Computes a square root of a modulo prime p
    :param a: the number to take the square root of
    :param k: positive integer, such that a^m = 1 (mod p) where m = (p-1)/(2^k)
    :param p: odd prime p modulo which we are working
    :param b: an arbitrary non-square modulo p
    :param b_inverse: the inverse of b modulo p, i.e., b * b_inverse = 1 (mod p)
    :return: one of the square roots of a modulo p (the other can be obtained via negation modulo p)
    """

    assert p > 2
    assert 0 < a < p
    assert k > 0

    m = (p - 1) >> k

    a_m = power_modulo(a, m, p)

    # assumption
    assert a_m == 1

    # check that b is indeed a non-square modulo p
    assert legendre_symbol(b, p) == p - 1

    k_delta = 0

    while m % 2 == 0:

        m >>= 1
        k_delta += 1

        assert m == (p - 1) >> k + k_delta

        a_m = power_modulo(a, m, p)

        if a_m == p - 1:
            # a^m = -1 (mod p)
            break

        # since Z/pZ is a field, there cannot be any roots for 1 apart from 1 and -1
        # the case -1 was already handled above
        assert a_m == 1
        # we simply continue dividing

    if a_m == p - 1:
        # a^m = -1 (mod p)
        assert k_delta >= 1
        assert k + k_delta >= 2

        b_power = 1 << (k + k_delta - 1)
        b_power_half = 1 << (k + k_delta - 2)

        assert power_modulo(a, m, p) == p - 1
        assert b_power * m == (p - 1) >> 1

        a_next = (a * power_modulo(b, b_power, p)) % p

        _logger.info("m = %d, a = %d, b = %d", m, a, b)
        _logger.debug("(a * b^%d)^m = (a * b^%d)^%d = %d^%d = 1", b_power, b_power, m, a_next, m)

        assert power_modulo(a_next, m, p) == 1

        a_next_root = _tonelli_shanks_recursive(a_next, k + k_delta, p, b, b_inverse)

        _logger.info("Backward propagation: root of %d is %d" % (a_next, a_next_root))

        a_root = a_next_root * power_modulo(b_inverse, b_power_half, p)

        return a_root % p

    assert a_m == 1
    assert m % 2 == 1

    # we now handle the case when m is odd
    # this case is easy, a^((m+1)/2) is a square root of a
    return power_modulo(a, (m + 1) >> 1, p)


def tonelli_shanks(a: int, p: int, /, *, deterministic=True) -> int | None:
    """
    Computes a square root of a modulo prime p
    :param a: the number to take the square root of
    :param p: odd prime p modulo which we are working
    :param deterministic: whether to search for the non-square b deterministically
    :return: one of the square roots of a modulo p (the other can be obtained via negation modulo p)
    """

    assert p > 2
    assert 0 < a < p
    # quick Fermat primality test
    assert power_modulo(a, p - 1, p) == 1

    if legendre_symbol(a, p) != 1:
        # a is not not a square modulo p
        return None

    b = _choose_b(p, det=deterministic)

    b_inverse = inverse_modulo(b, p)

    return _tonelli_shanks_recursive(a, 1, p, b, b_inverse)


def _main():
    _logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("[%(asctime)s %(levelname)7s]: %(message)s")

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    _logger.addHandler(console_handler)

    if len(sys.argv) < 3:
        _logger.error("Usage: python tonellishanks.py <a> <p>")
        _logger.error("- <a> is the number whose square root is to be computed")
        _logger.error("- <p> is the prime number modulo which the square root is to be taken")
        return

    a = int(sys.argv[1])
    p = int(sys.argv[2])

    _logger.info("a = %d, p = %d", a, p)

    if p < 3 or a >= p or a <= 0:
        _logger.error("Invalid input: recheck the a and p values you entered.")
        return

    if "--no-prime-test" not in sys.argv[1:] and not is_prime(p):
        _logger.error("p = %d is not a prime number", p)
        return

    _det = "--rnd" not in sys.argv[1:]

    _logger.info("Mode: %s", "deterministic" if _det else "randomized")

    root = tonelli_shanks(a, p, deterministic=_det)

    if root is None:
        _logger.info("%d is not a square modulo p = %d", a, p)
        return

    second_root = p - root

    if root > second_root:
        root, second_root = second_root, root

    _logger.info("The square roots of %d are: %d, %d", a, root, second_root)


if __name__ == "__main__":
    _main()
