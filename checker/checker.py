#!/usr/bin/env python
import logging
import os
import tempfile
import time

from pysat.formula import CNF

import config

gConsistencyCheckCounter = 0


def is_consistent(C: list) -> (bool, float):
    """
    Check if the given CNF formula is consistent using Choco Solver.
    :param C: a list of clauses
    :return: a tuple of two values:
        - a boolean value indicating whether the given CNF formula is consistent
        - the time taken to check the consistency
    """
    global gConsistencyCheckCounter

    # Create a temporary file for the CNF formula
    f = tempfile.NamedTemporaryFile()

    cnf = CNF()
    for clause in C:
        cnf.append(clause[1])
    cnf.to_file(f.name)  # Write the CNF formula to the temporary file

    start_time = time.time()
    p = os.popen("java -jar " + config.solver_path + " " + f.name)  # Run the solver
    out = p.read()
    total_time = time.time() - start_time

    f.close()  # close the temporary file
    p.close()  # close the process

    consistent = "UNSATISFIABLE" not in out
    logging.debug(">>> is_consistent [C={}, consistent={}]".format(C, consistent))
    return consistent, total_time
