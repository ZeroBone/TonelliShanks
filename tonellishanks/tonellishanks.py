import random

from euklidian import inverse_modulo
from powmod import power_modulo


def legendre_symbol(a: int, p: int, /) -> int:

    assert p % 2 != 0

    return power_modulo(a, (p - 1) >> 1, p)


def _choose_b(p: int, /, *, det=True) -> int:

    assert p % 2 != 0

    b = 2

    if det:
        while legendre_symbol(b, p) == 1:
            b += 1
    else:
        while legendre_symbol(b, p) == 1:
            b = random.randrange(2, p)

    assert b < p
    assert legendre_symbol(b, p) == p - 1

    return b


def _tonelli_shanks_recursive(a: int, k: int, p: int, b: int, /):
    """
    Computes a square root of a modulo prime p
    :param a: the number to take the square root of
    :param k: positive integer, such that a^m = 1 (mod p) where m = (p-1)/(2^k)
    :param p: odd prime p modulo which we are working
    :param b: an arbitrary non-square modulo p
    :return: one of the square roots of a modulo p (the other one is the negation)
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

        b_power = 1 << k_delta
        b_power_half = 1 << (k_delta - 1)

        assert power_modulo(a, m, p) == p - 1

        print("%d * %d = (p-1)/2" % (b_power, m))
        assert b_power * m == (p - 1) >> 1

        a_next = (a * power_modulo(b, b_power, p)) % p

        print(a, b_power, a_next)

        assert power_modulo(a_next, m, p) == 1

        a_next_root = _tonelli_shanks_recursive(a_next, k + k_delta - 1, p, b)

        a_root = a_next_root * inverse_modulo(power_modulo(b, b_power_half, p), p)

        return a_root % p

    assert a_m == 1
    assert m % 2 == 1

    # we now handle the case when m is odd
    # this case is easy, a^((m+1)/2) is a square root of a
    return power_modulo(a, (m + 1) >> 1, p)


def tonelli_shanks(a: int, p: int, /, *, deterministic=True) -> int | None:

    assert p > 2
    assert 0 < a < p
    # quick Fermat primality test
    assert power_modulo(a, p - 1, p) == 1

    if legendre_symbol(a, p) != 1:
        # a is not not a square modulo p
        return None

    b = _choose_b(p, det=deterministic)

    print("Chose b = %d" % b)

    return _tonelli_shanks_recursive(a, 1, p, b)


if __name__ == "__main__":

    result = tonelli_shanks(8, 17)

    print(result)
