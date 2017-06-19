import unittest

import tests.apiai_webhook_test

test_suits = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromModule(tests.apiai_webhook_test)
])

unittest.TextTestRunner(verbosity=2).run(test_suits)
