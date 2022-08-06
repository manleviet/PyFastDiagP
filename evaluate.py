#!/bin/python3
# import logging.config
import os
import time

# logging.config.fileConfig('logging.conf')

cards = ["1", "2", "4"]  # , "8", "16"]
lmaxs = ["0", "1", "2", "3", "4", "5"]
numScenarios = 10

start_time = time.time()
modelPath = "./data/linux/linux.cnf"
for card in cards:
    for i in range(numScenarios):
        reqPath = "./data/linux/prod_{}_{}.cnf".format(card, i + 1)
        for lmax in lmaxs:
            if lmax == "0":
                print(
                    "python3 ./eval_fastdiag.py " + modelPath + " " + reqPath)
                os.system(
                    "python3 ./eval_fastdiag.py " + modelPath + " " + reqPath + " >>" + " resultFastDiag.csv")
            else:
                print(
                    "python3 ./eval_fastdiagp_v1.py " + modelPath + " " + reqPath + " " + lmax)
                os.system(
                    "python3 ./eval_fastdiagp_v1.py " + modelPath + " " + reqPath + " " + lmax + " >>" + " resultFastDiagPV1.csv")

                print(
                    "python3 ./eval_fastdiagp_v2.py " + modelPath + " " + reqPath + " " + lmax)
                os.system(
                    "python3 ./eval_fastdiagp_v2.py " + modelPath + " " + reqPath + " " + lmax + " >>" + " resultFastDiagPV2.csv")

                print(
                    "python3 ./eval_fastdiagp_v3.py " + modelPath + " " + reqPath + " " + lmax)
                os.system(
                    "python3 ./eval_fastdiagp_v3.py " + modelPath + " " + reqPath + " " + lmax + " >>" + " resultFastDiagPV3.csv")

total_time = time.time() - start_time
print("Choco time: " + str(total_time))
