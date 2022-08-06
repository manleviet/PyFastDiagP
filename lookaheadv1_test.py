import logging.config
import multiprocessing as mp

from pysat.formula import CNF

from algorithms import fastdiagp_v1

logging.config.fileConfig('logging.conf')


def main():
    B_cnf = CNF(from_clauses=[[1]])
    C_cnf = CNF(from_clauses=[[2], [3], [4], [5]])

    B = sorted(enumerate(B_cnf.clauses, start=0), key=lambda x: x[0])
    C = sorted(enumerate(C_cnf.clauses, start=len(B_cnf.clauses)), key=lambda x: x[0])

    fastdiagp_v1.pool = mp.Pool(mp.cpu_count())

    fastdiagp_v1.lmax = 6
    fastdiagp_v1.lookahead(C, B, [], 0)


if __name__ == '__main__':
    main()
