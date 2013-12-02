import unittest
import pep8
import os

class Pep8Test(unittest.TestCase):
    top = os.path.join(os.path.dirname(__file__), '..', 'graphios_ng')

    def test_pep8(self):
        pep8style = pep8.StyleGuide()
        result = pep8style.check_files([os.path.abspath(self.top)])
        self.assertEqual(result.total_errors, 0,
                         "Pep8 found code style errors.")
