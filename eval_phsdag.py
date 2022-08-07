#!/usr/bin/env python
# import logging.config
import sys
import time
import multiprocessing as mp

from algorithms import phsdag
from checker import checker
from common.utils import prepare_cstrs_sets


# logging.config.fileConfig('logging.conf')


def main():
    if len(sys.argv) > 1:
        in_model_filename = sys.argv[1]
        in_req_filename = sys.argv[2]
        # fastdiagp_v1_1.numCores = int(sys.argv[3])
    else:
        # fastdiagp_v1_1.numCores = mp.cpu_count()
        in_model_filename = "./data/tests/test_model.cnf"
        in_req_filename = "./data/tests/test_prod_1.cnf"

    B, C = prepare_cstrs_sets(in_model_filename, in_req_filename)

    start_time = time.time()
    diag = phsdag.construct(B, C)
    total_time = time.time() - start_time

    # print(in_req_filename + "|" + str(total_time) + "|" + str(checker.counter_CC)
    #       + "|" + str(phsdag.counter_readyCC) + "|" + str(len(phsdag.lookupTable))
    #       + "|" + str(phsdag.numCores) + "|FastDiagP_V1|" + "|" + str(diag))

    print(in_req_filename + "|" + str(total_time) + "|" + str(checker.counter_CC)
          + "|PHSDAG|" + "|" + str(diag))


if __name__ == '__main__':
    main()