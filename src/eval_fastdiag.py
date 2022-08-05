#!/usr/bin/env python
import logging.config
import sys
import time

from common.utils import prepare_cstrs_sets
from src.algorithms.fastdiag import fastDiag
from src.checker.checker import gConsistencyCheckCounter

logging.config.fileConfig('logging.conf')


def main():
    if len(sys.argv) > 1:
        in_model_filename = sys.argv[1]
        in_req_filename = sys.argv[2]
        difficulty = int(sys.argv[5])

    else:  # Default values
        in_model_filename = "./data/tests/test_model.cnf"
        in_req_filename = "./data/tests/test_prod_1.cnf"
        difficulty = int(0)

    B, C = prepare_cstrs_sets(in_model_filename, in_req_filename)

    start_time = time.time()
    diag = fastDiag(C, B)
    total_time = time.time() - start_time

    print(in_model_filename + "|" + in_req_filename + "|" + str(total_time) + "|" + str(gConsistencyCheckCounter)
          + "|" + str(gConsistencyCheckCounter) + "|" + str(0) + "|fastdiag|" + "Choco" + "|" + str(difficulty)
          + "|" + str(diag))


if __name__ == '__main__':
    main()
