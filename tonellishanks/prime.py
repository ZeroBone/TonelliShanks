import random

from euklidian import gcd
from powmod import power_modulo


def is_prime(n: int) -> bool:
    if n <= 1:
        return False

    if n <= 3:
        return True

    if n % 2 == 0 or n % 3 == 0:
        return False

    # Fermat test
    for _ in range(n.bit_length() * 4):
        a = random.randrange(2, n)

        if gcd(a, n) != 1:
            return False

        if power_modulo(a, n - 1, n) != 1:
            return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i = i + 6

    return True


def next_prime(n: int) -> int:
    if n <= 1:
        return 2

    if n % 2 == 0:
        n = n + 1
        if is_prime(n):
            return n

    while True:
        n += 2
        if is_prime(n):
            return n
