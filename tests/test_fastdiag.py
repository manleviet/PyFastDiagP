import unittest

from algorithms import fastdiag, fastdiagp_v2
from algorithms import fastdiagp_v1
from common.utils import prepare_cstrs_sets

in_model_filename = "../data/tests/test_model.cnf"
in_req_filename = "../data/tests/test_prod_1.cnf"


class AlgorithmTests(unittest.TestCase):
    def test_fastdiag(self):
        B, C = prepare_cstrs_sets(in_model_filename, in_req_filename)

        fastdiag.solver_path = "../solver_apps/choco4solver.jar"
        diag = fastdiag.findDiagnosis(C, B)

        self.assertEqual("[(13, [-2]), (14, [-6])]", str(diag))

    def test_fastdiagp_v1(self):
        B, C = prepare_cstrs_sets(in_model_filename, in_req_filename)

        fastdiagp_v1.solver_path = "../solver_apps/choco4solver.jar"
        diag = fastdiagp_v1.findDiagnosis(C, B)

        self.assertEqual("[(13, [-2]), (14, [-6])]", str(diag))

    def test_fastdiagp_v2(self):
        B, C = prepare_cstrs_sets(in_model_filename, in_req_filename)

        fastdiagp_v2.solver_path = "../solver_apps/choco4solver.jar"
        diag = fastdiagp_v2.findDiagnosis(C, B)

        self.assertEqual("[(13, [-2]), (14, [-6])]", str(diag))


if __name__ == '__main__':
    unittest.main()
