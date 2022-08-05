#!/usr/bin/env python
import logging

from common import utils
from src.checker import checker

logging.basicConfig(level=logging.DEBUG)


def quickXplain(C, B):
    if checker.is_consistent(B + C)[0]:
        return "No Conflict"
    elif len(C) == 0:
        return []
    else:
        return QX(C, B, [])


def QX(C, B, Bo):
    if len(Bo) != 0 and not checker.is_consistent(B)[0]:
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
