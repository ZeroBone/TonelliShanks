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

    assert p > 2
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

    # assumption
    assert power_modulo(a, m, p) == 1

    a_m = 1

    # check that b is indeed a non-square modulo p
    assert legendre_symbol(b, p) == p - 1

    _logger.info("-------- [New round] --------")
    _logger.info("a = %d, m = %d, a^m = 1", a, m)

    while m % 2 == 0 and a_m == 1:

        m >>= 1
        k += 1

        assert m == (p - 1) >> k

        a_m = power_modulo(a, m, p)

        _logger.info(
            "m is even and a^m = 1 => we divide m by 2 and get: m = %d, a^m = %s",
            m,
            "1" if a_m == 1 else "-1"
        )

        # since Z/pZ is a field, there cannot be any roots for 1 apart from 1 and -1
        assert a_m == 1 or a_m == p - 1

    assert a_m == 1 or a_m == p - 1

    if a_m == p - 1:
        # a^m = -1 (mod p)

        _logger.info("m = %d, a^m = -1 => we multiply a^m with a legendre symbol of a non-square b modulo p", m)

        assert k >= 2

        b_power = 1 << (k - 1)
        b_power_half = 1 << (k - 2)

        assert power_modulo(a, m, p) == p - 1
        assert b_power * m == (p - 1) >> 1

        a_next = (a * power_modulo(b, b_power, p)) % p

        _logger.info("(a * b^%d)^m = (a * b^%d)^%d = %d^%d = 1", b_power, b_power, m, a_next, m)
        _logger.info(
            "It follows that a_next := a * b^%d = %d * %d = %d is a square whose root yields a root of a",
            b_power,
            a,
            power_modulo(b, b_power, p),
            a_next
        )

        assert power_modulo(a_next, m, p) == 1

        a_next_root = _tonelli_shanks_recursive(a_next, k, p, b, b_inverse)

        _logger.info("The root of a_next = %d is %d", a_next, a_next_root)

        a_root = a_next_root * power_modulo(b_inverse, b_power_half, p)

        _logger.info("sqrt(a_next)^2 = %d^2 = a_next = a * b^%d = sqrt(a)^2 * b^%d", a_next_root, b_power, b_power)
        _logger.info(
            "=> sqrt(a = %d) = sqrt(a_next) * b^(-%d) = %d * %d = %d",
            a,
            b_power_half,
            a_next_root,
            power_modulo(b_inverse, b_power_half, p),
            a_root
        )

        _logger.info("-------- [Round complete] --------")

        return a_root % p

    assert a_m == 1
    assert m % 2 == 1

    _logger.info("-------- [Round complete] --------")

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

    _logger.info("======== [Starting algorithm with a = %d, p = %d] ========", a, p)

    b = _choose_b(p, det=deterministic)

    b_inverse = inverse_modulo(b, p)

    assert b * b_inverse % p == 1

    return _tonelli_shanks_recursive(a, 1, p, b, b_inverse)


def _main():
    _logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    _logger.addHandler(console_handler)

    if len(sys.argv) < 3:
        _logger.error("Usage: python tonellishanks.py <a> <p>")
        _logger.error("- <a> is the number whose square root is to be computed")
        _logger.error("- <p> is the prime number modulo which the square root is to be taken")
        return

    a = int(sys.argv[1])
    p = int(sys.argv[2])

    if p < 3 or a >= p or a <= 0:
        _logger.info("Input values: a = %d, p = %d", a, p)
        _logger.error("Invalid input: recheck the a and p values you entered.")
        return

    if "--no-prime-test" not in sys.argv[1:] and not is_prime(p):
        _logger.error("p = %d is not a prime number", p)
        return

    _det = "--rnd" not in sys.argv[1:]

    _logger.info("Mode: %s", "deterministic" if _det else "randomized")

    root = tonelli_shanks(a, p, deterministic=_det)

    _logger.info("======== [Result] ========")

    if root is None:
        _logger.info("%d is not a square modulo p = %d", a, p)
        return

    second_root = p - root

    if root > second_root:
        root, second_root = second_root, root

    _logger.info("The square roots of %d are: %d, %d", a, root, second_root)


if __name__ == "__main__":
    _main()
