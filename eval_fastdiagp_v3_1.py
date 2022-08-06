#!/usr/bin/env python
# import logging.config
import sys
import time
import multiprocessing as mp

from algorithms import fastdiagp_v3_1
from checker import checker
from common.utils import prepare_cstrs_sets


# logging.config.fileConfig('logging.conf')


def main():
    if len(sys.argv) > 1:
        in_model_filename = sys.argv[1]
        in_req_filename = sys.argv[2]
        fastdiagp_v3_1.numCores = int(sys.argv[3])
    else:
        fastdiagp_v3_1.numCores = mp.cpu_count()
        in_model_filename = "./data/tests/test_model.cnf"
        in_req_filename = "./data/tests/test_prod_1.cnf"

    B, C = prepare_cstrs_sets(in_model_filename, in_req_filename)

    start_time = time.time()
    diag = fastdiagp_v3_1.findDiagnosis(C, B)
    total_time = time.time() - start_time

    print(in_req_filename + "|" + str(total_time) + "|" + str(checker.counter_CC)
          + "|" + str(fastdiagp_v3_1.counter_readyCC) + "|" + str(len(fastdiagp_v3_1.lookupTable))
          + "|" + str(fastdiagp_v3_1.numCores) + "|FastDiagP_V3|" + "|" + str(diag))


if __name__ == '__main__':
    main()
