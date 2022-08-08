#!/usr/bin/env python
# import logging.config
import multiprocessing as mp
import sys
import time

from algorithms import levelp_hsdag
from checker import checker
from common.utils import prepare_cstrs_sets


# logging.config.fileConfig('logging.conf')


def main():
    if len(sys.argv) > 1:
        in_model_filename = sys.argv[1]
        in_req_filename = sys.argv[2]
        levelp_hsdag.solver_path = sys.argv[3]
        levelp_hsdag.numCores = int(sys.argv[4])
    else:
        levelp_hsdag.numCores = mp.cpu_count()
        in_model_filename = "./data/tests/test_model.cnf"
        in_req_filename = "./data/tests/test_prod_1.cnf"
        levelp_hsdag.solver_path = "solver_apps/org.sat4j.core.jar"

    B, C = prepare_cstrs_sets(in_model_filename, in_req_filename)

    levelp_hsdag.maxNumberOfDiagnoses = 1  # stop after first diagnosis

    start_time = time.time()
    levelp_hsdag.construct(B, C)
    diag = levelp_hsdag.getDiagnoses()
    total_time = time.time() - start_time

    print(in_req_filename + "|" + str(total_time) + "|" + str(checker.counter_CC)
          + "|" + str(0) + "|" + str(levelp_hsdag.counter_constructed_nodes)
          + "|" + str(levelp_hsdag.numCores) + "|LevelP_HSDAG|" + levelp_hsdag.solver_path + "|" + str(diag))


if __name__ == '__main__':
    main()
