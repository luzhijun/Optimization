import unittest

import test_canonicalization 
import test_e2e_client 
import test_functions 
import test_jsonizable 

def suite():
    load = unittest.TestLoader().loadTestsFromModule
    modules = [
        test_canonicalization,
        test_e2e_client,
        test_functions,
        test_jsonizable,
    ]
    suites = unittest.TestSuite(map(load, modules))
    return suites

if __name__ == '__main__':
    s = suite()
    unittest.TextTestRunner(verbosity=2).run(s)
