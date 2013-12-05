import unittest
from graphios_ng import utils


class WithLogTest(unittest.TestCase):
    def test_with_log(self):
        @utils.with_log
        def testing(log=None):
            self.assertIsNotNone(log)
            self.assertEquals(str(type(log)), "<class 'logging.Logger'>")
        testing()

    def test_with_log_overwrite(self):
        @utils.with_log
        def testing(log=None):
            self.assertEquals(log, 'Should not change')
        testing(log = 'Should not change')
