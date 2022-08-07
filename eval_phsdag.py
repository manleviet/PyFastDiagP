#!/usr/bin/env python
import logging.config
import sys
import time

from algorithms import phsdag
from checker import checker
from common.utils import prepare_cstrs_sets


logging.config.fileConfig('logging.conf')


def main():
    if len(sys.argv) > 1:
        in_model_filename = sys.argv[1]
        in_req_filename = sys.argv[2]
        phsdag.solver_path = sys.argv[3]
        phsdag.numCores = int(sys.argv[4])
    else:
        in_model_filename = "./data/tests/test_model.cnf"
        in_req_filename = "./data/tests/test_prod_1.cnf"
        phsdag.solver_path = "solver_apps/org.sat4j.core.jar"
        phsdag.numCores = 8

    B, C = prepare_cstrs_sets(in_model_filename, in_req_filename)

    phsdag.maxNumberOfDiagnoses = 1  # stop after first diagnosis

    start_time = time.time()
    diag = phsdag.construct(B, C)
    total_time = time.time() - start_time

    print(in_req_filename + "|" + str(total_time) + "|" + str(checker.counter_CC)
          + "|" + str(0) + "|" + str(phsdag.counter_constructed_nodes)
          + "|" + str(phsdag.numCores) + "|FastDiagP_V2_1|" + phsdag.solver_path + "|" + str(diag))


if __name__ == '__main__':
    main()
