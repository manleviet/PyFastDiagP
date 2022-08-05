import unittest

import config
from algorithms.fastdiag import fastDiag
from common.utils import prepare_cstrs_sets

in_model_filename = "../data/tests/test_model.cnf"
in_req_filename = "../data/tests/test_prod_1.cnf"

config.solver_path = "../solver_apps/choco4solver.jar"


class AlgorithmTests(unittest.TestCase):
    def test_fastdiag(self):
        B, C = prepare_cstrs_sets(in_model_filename, in_req_filename)

        diag = fastDiag(C, B)

        self.assertEqual("[(13, [-2]), (14, [-6])]", str(diag))


if __name__ == '__main__':
    unittest.main()
