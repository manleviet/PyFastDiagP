#!/usr/bin/env python
import logging
import sys
import time

from pysat.formula import CNF

from algorithms.fd import fastDiag
from checker.checker import counter_consistency_check

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("test.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def main():
    if len(sys.argv) > 1:
        mode_file = sys.argv[1]
        requirement_file = sys.argv[2]
        lmax = int(sys.argv[3])
        solver = sys.argv[4]
        difficulty = int(sys.argv[5])

    else:  # Default values
        lmax = int(0)
        requirement_file = "data/tests/test_prod_1.cnf"
        mode_file = "data/tests/test_model.cnf"
        solver = "Sat4j"
        difficulty = int(0)

    modelCNF = CNF(from_file=mode_file)
    requirementsCNF = CNF(from_file=requirement_file)

    C_cnf = CNF(from_clauses=modelCNF.clauses[1:])
    C_cnf.extend(requirementsCNF.clauses)

    B_cnf = CNF(from_clauses=modelCNF.clauses[0:1])

    print("C_cnf:")
    for clause in C_cnf.clauses:
        print(clause)

    B = sorted(enumerate(B_cnf.clauses), key=lambda x: x[0])
    C = sorted(enumerate(C_cnf.clauses, len(B_cnf.clauses)), key=lambda x: x[0])

    print("C:")
    for clause in C:
        print(clause)

    start_time = time.time()
    result = fastDiag(C, B)
    total_time = time.time() - start_time

    print(mode_file + "|" + requirement_file + "|" + str(total_time) + "|" + str(counter_consistency_check) + "|" + str(
        counter_consistency_check) + "|" + str(
        lmax) + "|algorithms|" + solver + "|" + str(difficulty) + "|" + str(result))


if __name__ == '__main__':
    main()
