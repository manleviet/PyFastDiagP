#!/usr/bin/env python
import multiprocessing as mp
import time

from algorithms import fastdiagp_v1, fastdiag, fastdiagp_v2, fastdiagp_v3, fastdiagp_v1_1, fastdiagp_v2_1, \
    fastdiagp_v3_1
from checker import checker
from common.utils import prepare_cstrs_sets


# logging.config.fileConfig('logging.conf')


def main():
    in_model_filename = "data/linux/linux.cnf"
    in_req_filename = "data/linux/prod_1_1.cnf"

    fastdiagp_v1.lmax = int(6)
    fastdiagp_v2.lmax = int(6)
    fastdiagp_v3.lmax = int(6)

    fastdiagp_v1.solver_path = "solver_apps/org.sat4j.core.jar"
    fastdiagp_v2.solver_path = "solver_apps/org.sat4j.core.jar"
    fastdiagp_v3.solver_path = "solver_apps/org.sat4j.core.jar"

    fastdiagp_v1_1.numCores = mp.cpu_count()
    fastdiagp_v2_1.numCores = mp.cpu_count()
    fastdiagp_v3_1.numCores = mp.cpu_count()

    fastdiagp_v1_1.solver_path = "solver_apps/org.sat4j.core.jar"
    fastdiagp_v2_1.solver_path = "solver_apps/org.sat4j.core.jar"
    fastdiagp_v3_1.solver_path = "solver_apps/org.sat4j.core.jar"

    B, C = prepare_cstrs_sets(in_model_filename, in_req_filename)

    start_time = time.time()
    diag = fastdiag.findDiagnosis(C, B)
    total_time = time.time() - start_time

    print(in_req_filename + "|" + str(total_time) + "|" + str(checker.counter_CC)
          + "|" + str(0) + "|" + str(0)
          + "|" + str(0) + "|fastdiag|" + "|" + fastdiag.solver_path + "|" + str(diag))

    start_time = time.time()
    diag = fastdiagp_v1.findDiagnosis(C, B)
    total_time = time.time() - start_time

    print(in_req_filename + "|" + str(total_time) + "|" + str(checker.counter_CC)
          + "|" + str(fastdiagp_v1.counter_readyCC) + "|" + str(len(fastdiagp_v1.lookupTable))
          + "|" + str(fastdiagp_v1.lmax) + "|FastDiagP_V1|" + "|" + fastdiagp_v1.solver_path + "|" + str(diag))

    start_time = time.time()
    diag = fastdiagp_v2.findDiagnosis(C, B)
    total_time = time.time() - start_time

    print(in_req_filename + "|" + str(total_time) + "|" + str(checker.counter_CC)
          + "|" + str(fastdiagp_v2.counter_readyCC) + "|" + str(len(fastdiagp_v2.lookupTable))
          + "|" + str(fastdiagp_v2.lmax) + "|FastDiagP_V2|" + "|" + fastdiagp_v2.solver_path + "|" + str(diag))

    start_time = time.time()
    diag = fastdiagp_v3.findDiagnosis(C, B)
    total_time = time.time() - start_time

    print(in_req_filename + "|" + str(total_time) + "|" + str(checker.counter_CC)
          + "|" + str(fastdiagp_v3.counter_readyCC) + "|" + str(len(fastdiagp_v3.lookupTable))
          + "|" + str(fastdiagp_v3.lmax) + "|FastDiagP_V3|" + "|" + fastdiagp_v3.solver_path + "|" + str(diag))

    start_time = time.time()
    diag = fastdiagp_v1_1.findDiagnosis(C, B)
    total_time = time.time() - start_time

    print(in_req_filename + "|" + str(total_time) + "|" + str(checker.counter_CC)
          + "|" + str(fastdiagp_v1_1.counter_readyCC) + "|" + str(len(fastdiagp_v1_1.lookupTable))
          + "|" + str(fastdiagp_v1_1.numCores) + "|FastDiagP_V1_1|" + fastdiagp_v1_1.solver_path + "|" + str(diag))

    start_time = time.time()
    diag = fastdiagp_v2_1.findDiagnosis(C, B)
    total_time = time.time() - start_time

    print(in_req_filename + "|" + str(total_time) + "|" + str(checker.counter_CC)
          + "|" + str(fastdiagp_v2_1.counter_readyCC) + "|" + str(len(fastdiagp_v2_1.lookupTable))
          + "|" + str(fastdiagp_v2_1.numCores) + "|FastDiagP_V2_1|" + fastdiagp_v2_1.solver_path + "|" + str(diag))

    start_time = time.time()
    diag = fastdiagp_v3_1.findDiagnosis(C, B)
    total_time = time.time() - start_time

    print(in_req_filename + "|" + str(total_time) + "|" + str(checker.counter_CC)
          + "|" + str(fastdiagp_v3_1.counter_readyCC) + "|" + str(len(fastdiagp_v3_1.lookupTable))
          + "|" + str(fastdiagp_v3_1.numCores) + "|FastDiagP_V3_1|" + fastdiagp_v3_1.solver_path + "|" + str(diag))

if __name__ == '__main__':
    main()
