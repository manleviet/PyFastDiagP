#!/usr/bin/env python
# import logging.config
import sys
import time

from algorithms import fastdiagp_v1
from checker import checker
from common.utils import prepare_cstrs_sets


# logging.config.fileConfig('logging.conf')


def main():
    if len(sys.argv) > 1:
        in_model_filename = sys.argv[1]
        in_req_filename = sys.argv[2]
        fastdiagp_v1.solver_path = sys.argv[3]
        fastdiagp_v1.lmax = int(sys.argv[4])
    else:
        fastdiagp_v1.lmax = int(6)
        in_model_filename = "./data/tests/test_model.cnf"
        in_req_filename = "./data/tests/test_prod_1.cnf"
        fastdiagp_v1.solver_path = "solver_apps/org.sat4j.core.jar"

    B, C = prepare_cstrs_sets(in_model_filename, in_req_filename)

    start_time = time.time()
    diag = fastdiagp_v1.findDiagnosis(C, B)
    total_time = time.time() - start_time

    print(in_req_filename + "|" + str(total_time) + "|" + str(checker.counter_CC)
          + "|" + str(fastdiagp_v1.counter_readyCC) + "|" + str(len(fastdiagp_v1.lookupTable))
          + "|" + str(fastdiagp_v1.lmax) + "|FastDiagP_V1|" + fastdiagp_v1.solver_path + "|" + str(diag))


if __name__ == '__main__':
    main()
