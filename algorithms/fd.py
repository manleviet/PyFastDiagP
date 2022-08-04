#!/usr/bin/env python
"""Implementation of FastDiag algorithm."""

import logging

from algorithms import utils
from checker import checker


def fastDiag(C, B):
    logging.info("fastDiag [C={}, B={}]".format(C, B))

    # if callConsistencyCheck(B + C):
    if checker.isConsistency(B + C)[0]:
        logging.info("No Diagnosis".format(C))
        return "No Diagnosis"
    elif len(C) == 0:
        logging.info("return {}".format([]))
        return []
    else:
        mss = fd([], C, B)
        diag = utils.diff(C, mss)
        logging.info("return {}".format(diag))
        return diag


def fd(Δ, C, B):
    logging.debug(">>> FD [Δ={}, C={}, B={}]".format(Δ, C, B))

    # if len(Δ) != 0 and callConsistencyCheck(B + C):
    if len(Δ) != 0 and checker.isConsistency(B + C)[0]:
        logging.debug("<<< return {}".format(C))
        return C

    # n = len(C)
    if len(C) == 1:
        logging.debug("<<< return Φ")
        return []

    # C1 = {c1..ck}; C2 = {ck + 1..cn};
    # k = int(n / 2)
    # C1 = C[:k]
    # C2 = C[k:]

    C1, C2 = utils.split(C)

    # Δ1 = FD(C2, C1, B)
    Δ1 = fd(C2, C1, B)
    # Δ2 = FD(C1 - Δ1, C2, B U Δ1);
    C1withoutΔ1 = utils.diff(C1, Δ1)
    Δ2 = fd(C1withoutΔ1, C2, B + Δ1)

    # return Δ1 + Δ2
    Δ = Δ1 + Δ2
    logging.debug("<<< return {}".format(Δ))
    return Δ
