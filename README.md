# TonelliShanks

This project is an implementation of the Tonelli-Shanks algorithm for computing square roots modulo a prime number. In other words, given an odd prime $ p $ and a number $ a \in (\mathbb{Z}/p\mathbb{Z})^* $, the algorithm tests whether $ a $ is a quadratic residue modulo $ p $, and if this is the case, computes $ b \in (\mathbb{Z}/p\mathbb{Z})^* $ such that:

$$
b^2 \equiv a \mod p
$$
