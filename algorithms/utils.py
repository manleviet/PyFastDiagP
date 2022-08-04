#!/usr/bin/env python
"""Provides utility functions for processing list of CNF clauses."""


def get_hash(C, len_B):
    """
    Returns the hash of the given CNF formula.
    :param C: a list of clauses
    :param len_B: the number of clauses in the background knowledge
    :return: the hash of the given CNF formula
    """
    C = sorted([i for i in C if i[0] >= len_B], key=lambda x: x[0])
    return str(C)


def diff(x: list, y: list) -> list:
    """
    Returns the difference of two lists.
    :param x: list
    :param y: list
    :return: list
    """
    return [item for item in x if item not in y]


def split(C: list) -> (list, list):
    """
    Splits the given CNF formula into two parts.
    :param C: a list of clauses
    :return: a tuple of two lists
    """
    len_B = len(C) // 2
    return C[:len_B], C[len_B:]
