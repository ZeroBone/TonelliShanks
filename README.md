# TonelliShanks

This project is an implementation of the [Tonelli-Shanks algorithm](https://en.wikipedia.org/wiki/Tonelli%E2%80%93Shanks_algorithm) for computing square roots modulo a prime number. In other words, given an odd prime $p$ and a number $a \in (\mathbb{Z}/p\mathbb{Z})^{\star}$, the algorithm tests whether $a$ is a quadratic residue modulo $p$, and if this is the case, computes $b \in (\mathbb{Z}/p\mathbb{Z})^{\star}$ such that:

$$
b^2 \equiv a \mod p
$$

The Tonelli-Shanks algorithm may need to compute a non-square modulo $p$ in order to correctly handle the case when $a^m \equiv -1 \mod p$ for some $m$ dividing $(p-1)/2$. In that case, two modes are implemented: *deterministic* and *randomized*. In the deterministic mode, as the name suggests, the algorithm is completely deterministic and computes the non-square modulo $p$ by simply trying out all values between $2$ and $p-1$ and testing whether the current value is a non-square using [Euler's criterion](https://en.wikipedia.org/wiki/Euler%27s_criterion). In the randomized mode, the same is done more efficiently by using a preudo-random number generator to search for the non-square. Since exactly half of the elements of $(\mathbb{Z}/p\mathbb{Z})^{\star}$ are squares and the other half are non-squares, it follows that 2 is the expected number of iterations needed to find the non-square modulo $p$. This implies that the expected time complexity of the entire algorithm is $O(\log(p)^2)$ (in the randomized mode).

## Installation

**Recommended python version**: 3.10.x or higher

**Dependencies**: none

## Usage

To run the tool, execute

```bash
python tonellishanks/tonellishanks.py <a> <p>
```

where `<a>` is $a\in(\mathbb{Z}/p\mathbb{Z})^{\star}$ and `<p>` is $p$, followed by the following possible command line arguments:

* `--rnd` makes the algorithm run in randomized mode (see above).
* `--no-prime-test` disables the testing whether $p$ is a prime, prior to executing the algorithm. Add this argument to avoid performance issues when $p$ is large.

The implementation of the algorithm can also be invoked via the Python API

```python
def tonelli_shanks(a: int, p: int, /, *, deterministic=True) -> int | None
```

where the `deterministic` argument should be set to true iff the algorithm is to be run in deterministic mode.

**Important**: the caller of this function must guarantee that $p$ is an odd prime and that $1 \le a \le p-1$.

### Tests

This project is thoroughly tested using unit tests together with a lot of regular assertions verifying that the invariants are maintained throughout the execution. Unit tests can be run via the

```bash
python tonellishanks/test.py
```

command.

### Example

If executed from the CLI, this tool also produces a detailed log of how the square root was computed. This may be useful for educational purposes. For example, running the tool to compute the square roots of $a=8$ modulo $p=17$ produces:

```
Mode: deterministic
======== [Starting algorithm with a = 8, p = 17] ========
Found b = 3 after 2 attempts
-------- [New round] --------
a = 8, m = 8, a^m = 1
m is even and a^m = 1 => we divide m by 2 and get: m = 4, a^m = -1
m = 4, a^m = -1 => we multiply a^m with a legendre symbol of a non-square b modulo p
(a * b^2)^m = (a * b^2)^4 = 4^4 = 1
It follows that a_next := a * b^2 = 8 * 9 = 4 is a square whose root yields a root of a
-------- [New round] --------
a = 4, m = 4, a^m = 1
m is even and a^m = 1 => we divide m by 2 and get: m = 2, a^m = -1
m = 2, a^m = -1 => we multiply a^m with a legendre symbol of a non-square b modulo p
(a * b^4)^m = (a * b^4)^2 = 1^2 = 1
It follows that a_next := a * b^4 = 4 * 13 = 1 is a square whose root yields a root of a
-------- [New round] --------
a = 1, m = 2, a^m = 1
m is even and a^m = 1 => we divide m by 2 and get: m = 1, a^m = 1
-------- [Round complete] --------
The root of a_next = 1 is 1
sqrt(a_next)^2 = 1^2 = a_next = a * b^4 = sqrt(a)^2 * b^4
=> sqrt(a = 4) = sqrt(a_next) * b^(-2) = 1 * 2 = 2
-------- [Round complete] --------
The root of a_next = 4 is 2
sqrt(a_next)^2 = 2^2 = a_next = a * b^2 = sqrt(a)^2 * b^2
=> sqrt(a = 8) = sqrt(a_next) * b^(-1) = 2 * 6 = 12
-------- [Round complete] --------
======== [Result] ========
The square roots of 8 are: 5, 12
```

## Copyright

Copyright (c) 2022 Alexander Mayorov.

This project is licensed under the MIT License. Please leave a license and copyright notice if you use this software. See the `LICENSE` file for more details.
