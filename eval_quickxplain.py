#!/usr/bin/env python
import logging.config
import sys
import time

from algorithms.quickxplain import quickXplain
from checker import checker
from common.utils import prepare_cstrs_sets

logging.config.fileConfig('logging.conf')


def main():
    if len(sys.argv) > 1:
        in_model_filename = sys.argv[1]
        in_req_filename = sys.argv[2]

    else:  # Default values
        in_model_filename = "./data/tests/test_model.cnf"
        in_req_filename = "./data/tests/test_prod_1.cnf"

    B, C = prepare_cstrs_sets(in_model_filename, in_req_filename)

    start_time = time.time()
    conflict = quickXplain(C, B)
    total_time = time.time() - start_time

    print(in_model_filename + "|" + in_req_filename + "|" + str(total_time) + "|" + str(checker.counter_CC)
          + "|" + str(0) + "|quickxplain|" + "Choco" + "|" + str(conflict))


if __name__ == '__main__':
    main()
