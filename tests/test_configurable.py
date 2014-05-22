import unittest
from graphios_ng.configurable import Configurable


class ConfigurableTest(unittest.TestCase):
    def test_missing_config(self):
        class Test(Configurable):
            required_config = ['test']

        with self.assertRaises(ValueError):
            Test(config = {})

    def test_matching_config(self):
        class Test(Configurable):
            required_config = ['test']

        t = Test(config = {'test': 'foobar'})
        self.assertEqual(t.get_config('test'), 'foobar')

    def test_extra_config(self):
        class Test(Configurable):
            required_config = ['test']

        t = Test(config = {'test': 'foobar', 'test2': 'foo'})
        self.assertEqual(t.get_config('test'), 'foobar')
        self.assertEqual(t.get_config('test2'), 'foo')

    def test_default_config(self):
        class Test(Configurable):
            pass

        t = Test(config = {'test': 'foobar'})
        self.assertEqual(t.get_config('test'), 'foobar')
        self.assertEqual(t.get_config('test2', 'foobar'), 'foobar')
        self.assertIsNone(t.get_config('test2'))
