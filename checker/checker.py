#!/usr/bin/env python
import os
import tempfile
import time

from pysat.formula import CNF

counter_consistency_check = 0

def isConsistency(C: list) -> (bool, float):
    """
    Check if the given CNF formula is consistent using
    :param C: a list of clauses
    :return:
    """
    global counter_consistency_check

    f = tempfile.NamedTemporaryFile()

    cnf = CNF()
    for clause in C:
        cnf.append(clause[1])
    cnf.to_file(f.name)

    start_time = time.time()
    out = os.popen("java -jar apps/choco4solver.jar " + f.name).read()
    f.close()
    total_time = time.time() - start_time

    return "UNSATISFIABLE" not in out, total_time
