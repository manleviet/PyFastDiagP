#!/usr/bin/env python
"""
Breadth first search approach
The assumption of consistency of B U C is taken into account first

Run the consistency check on the main thread, if it doesn't exist in the lookup table.
"""
import logging
import multiprocessing as mp

from checker import checker
from common import utils

lookupTable = {}
counter_readyCC = 0
lmax = 4
pool = None

solver_path = "solver_apps/choco4solver.jar"

genhash = ""


def findDiagnosis(C: list, B: list) -> list:
    """
    Activate FastDiag algorithm if there exists at least one constraint,
    which induces an inconsistency in B. Otherwise, it returns an empty set.

    // Func FastDiag(C, B) : Δ
    // if isEmpty(C) or consistent(B U C) return Φ
    // else return C \\ FD(Φ, C, B)
    :param C: a consideration set of constraints
    :param B: a background knowledge
    :return: a diagnosis or an empty set
    """
    global pool

    logging.info("fastDiag [C={}, B={}]".format(C, B))

    # if isEmpty(C) or consistent(B U C) return Φ
    if len(C) == 0 or checker.is_consistent(B + C, solver_path)[0]:
        logging.info("return Φ")
        return []
    else:  # return C \ FD(C, B, Φ)
        pool = mp.Pool(mp.cpu_count())

        mss = fd([], C, B)
        diag = utils.diff(C, mss)

        pool.close()
        pool.terminate()

        logging.info("return {}".format(diag))
        return diag


def fd(Δ: list, C: list, B: list) -> list:
    """
    The implementation of MSS-based FastDiag algorithm.
    The algorithm determines a maximal satisfiable subset MSS (Γ) of C U B.

    // Func FD(Δ, C = {c1..cn}, B) : MSS
    // if Δ != Φ and consistent(B U C) return C;
    // if singleton(C) return Φ;
    // k = n/2;
    // C1 = {c1..ck}; C2 = {ck+1..cn};
    // Δ1 = FD(C2, C1, B);
    // Δ2 = FD(C1 - Δ1, C2, B U Δ1);
    // return Δ1 ∪ Δ2;
    :param Δ: check to skip redundant consistency checks
    :param C: a consideration set of constraints
    :param B: a background knowledge
    :return: a maximal satisfiable subset MSS of C U B
    """
    logging.debug(">>> FD [Δ={}, C={}, B={}]".format(Δ, C, B))

    # if Δ != Φ and consistent(B U C) return C;
    if len(Δ) != 0 and is_consistent_with_lookahead(C, B, Δ)[0]:
        logging.debug("<<< return {}".format(C))
        return C

    # if singleton(C) return Φ;
    if len(C) == 1:
        logging.debug("<<< return Φ")
        return []

    # C1 = {c1..ck}; C2 = {ck+1..cn};
    C1, C2 = utils.split(C)

    # Δ1 = FD(C2, C1, B);
    Δ1 = fd(C2, C1, B)
    # Δ2 = FD(C1 - Δ1, C2, B U Δ1);
    C1withoutΔ1 = utils.diff(C1, Δ1)
    Δ2 = fd(C1withoutΔ1, C2, B + Δ1)

    logging.debug("<<< return [Δ1={} ∪ Δ2={}]".format(Δ1, Δ2))

    # return Δ1 + Δ2
    return Δ1 + Δ2


def is_consistent_with_lookahead(C, B, Δ) -> (bool, float):
    """
    If the consistency check doesn't exist in the lookup table,
    we run lookahead on a thread. Besides, we run the consistency check
    on the main thread.
    """
    global pool, genhash

    BwithC = B + C

    genhash = hashcode = utils.get_hashcode(BwithC)
    if not (hashcode in lookupTable):

        lookupTable.update({hashcode: True})

        pool.apply_async(lookahead, args=([C, B, [Δ], 0]))
        # lookahead(C, B, [Δ], 0)

        result = checker.is_consistent(BwithC, solver_path)

        # lookupTable.update({hashcode: result})

        return result
    else:
        return lookup_CC(hashcode)


def lookup_CC(hashcode: str) -> (bool, float):
    global counter_readyCC, lookupTable

    result = lookupTable.get(hashcode)

    if result.ready():  # result is not None and
        counter_readyCC = counter_readyCC + 1
    return result.get()


def lookahead(C, B, Δ, level):
    global lookupTable, pool, genhash

    logging.debug(">>> lookahead [l={}, Δ={}, C={}, B={}]".format(level, Δ, C, B))

    if level < lmax:
        BwithC = B + C

        if genhash == "":
            hashcode = utils.get_hashcode(BwithC)
        else:
            hashcode = genhash
            genhash = ""

        if not (hashcode in lookupTable):
            future = pool.apply_async(checker.is_consistent, args=([BwithC, solver_path]))
            lookupTable.update({hashcode: future})

            logging.debug(">>> addCC [l={}, C={}]".format(level, hashcode))

        # B U C assumed consistent
        if len(Δ) > 1:  # and len(Δ[0]) == 1:
            hashcode = utils.get_hashcode(BwithC + Δ[0])
            if hashcode in lookupTable:  # case 2.1
                Δ2l, Δ2r = utils.split(Δ[1])
                Δ_prime = Δ.copy()
                del Δ_prime[0]
                del Δ_prime[0]
                Δ_prime.insert(0, Δ2r)

                # LookAhead(Δ2l, B U C, Δ2r U (Δ \ {Δ1, Δ2})), l + 1)
                lookahead(Δ2l, BwithC, Δ_prime, level + 1)
        elif len(Δ) >= 1 and len(Δ[0]) == 1:  # case 2.2
            Δ1 = Δ[0]
            Δ_prime = Δ.copy()
            del Δ_prime[0]

            # LookAhead(Δ1, B U C, Δ \ {Δ1}, l + 1)
            lookahead(Δ1, BwithC, Δ_prime, level + 1)
        elif len(Δ) >= 1 and len(Δ[0]) > 1:  # case 2.3
            Δ1l, Δ1r = utils.split(Δ[0])
            Δ_prime = Δ.copy()
            del Δ_prime[0]
            Δ_prime.insert(0, Δ1r)

            # LookAhead(Δ1l, B U C, Δ1r U (Δ \ {Δ1})), l + 1)
            lookahead(Δ1l, BwithC, Δ_prime, level + 1)

        # B U C assumed inconsistent
        if len(C) > 1:  # case 1.1
            Cl, Cr = utils.split(C)
            Δ_prime = Δ.copy()
            Δ_prime.insert(0, Cr)

            # LookAhead(Cl, B, Cr U Δ, l + 1)
            lookahead(Cl, B, Δ_prime, level + 1)
        elif len(C) == 1 and len(Δ) >= 1 and len(Δ[0]) == 1:  # case 1.2
            Δ1 = Δ[0]
            Δ_prime = Δ.copy()
            del Δ_prime[0]

            # LookAhead(Δ1, B, Δ \ {Δ1}, l + 1)
            lookahead(Δ1, B, Δ_prime, level + 1)
        elif len(C) == 1 and len(Δ) >= 1 and len(Δ[0]) > 1:  # case 1.3
            Δ1l, Δ1r = utils.split(Δ[0])
            Δ_prime = Δ.copy()
            del Δ_prime[0]
            Δ_prime.insert(0, Δ1r)

            # LookAhead(Δ1l, B, Δ1r U (Δ \ {Δ1})), l + 1)
            lookahead(Δ1l, B, Δ_prime, level + 1)
