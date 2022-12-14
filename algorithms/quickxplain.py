#!/usr/bin/env python
# import logging

from checker import checker
from common import utils

# logging.basicConfig(level=logging.DEBUG)

solver_path = "solver_apps/choco4solver.jar"

def quickXplain(C, B):
    if checker.is_consistent(B + C, solver_path)[0]:
        return []
    elif len(C) == 0:
        return []
    else:
        return QX(C, B, [])


def QX(C, B, Bo):
    if len(Bo) != 0 and not checker.is_consistent(B, solver_path)[0]:
        return []

    if len(C) == 1:
        return C

    # k = int(len(C) / 2)
    # Ca = C[0:k]
    # Cb = C[k:len(C)]
    Ca, Cb = utils.split(C)

    A2 = QX(Ca, (B + Cb), Cb)
    A1 = QX(Cb, (B + A2), A2)

    return A1 + A2
