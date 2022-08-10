#!/bin/python3
# import logging.config
import os
import time

# logging.config.fileConfig('logging.conf')

cards = ["1", "2", "4", "8", "16"]
# lmaxs = ["0"]  # , "1", "2", "3", "4", "5"]
cores = ["2", "4", "6", "8"]
numScenarios = 10

solver_path = "solver_apps/org.sat4j.core.jar"

start_time = time.time()
modelPath = "./data/linux/linux.cnf"
for card in cards:
    for i in range(numScenarios):
        reqPath = "./data/linux/prod_{}_{}.cnf".format(card, i + 1)

        for core in cores:
            print(
                "python3 ./eval_fastdiagp_v1_1.py " + modelPath + " " + reqPath + " " + solver_path + " " + core)
            os.system(
                "python3 ./eval_fastdiagp_v1_1.py " + modelPath + " " + reqPath + " " + solver_path + " " + core + " >>" + " resultFastDiagPV1_1.csv")

total_time = time.time() - start_time
print("Sat4j time: " + str(total_time))
