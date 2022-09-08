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

#### Copyright

Copyright (c) 2022 Alexander Mayorov.

This project is licensed under the MIT License. Please leave a license and copyright notice if you use this software. See the `LICENSE` file for more details.
