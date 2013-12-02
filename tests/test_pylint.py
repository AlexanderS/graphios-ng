import unittest
import os
import sys
from pylint import lint
from pylint.reporters.text import TextReporter

class PylintTest(unittest.TestCase):
    top = os.path.join(os.path.dirname(__file__), '..')

    def test_pylint(self):
        rcfile = os.path.abspath(os.path.join(self.top, 'tests', 'pylint.rc'))
        args = ['--rcfile=' + rcfile, os.path.join(self.top, 'graphios_ng')]
        reporter = TextReporter(output=sys.stdout)
        result = lint.Run(args=args, reporter=reporter, exit=False)
        self.assertEqual(result.linter.msg_status, 0,
                         "Pylint found code style errors.")
