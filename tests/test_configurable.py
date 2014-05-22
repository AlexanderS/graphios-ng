import unittest
from graphios_ng.configurable import Configurable


class ConfigurableTest(unittest.TestCase):
    def test_missing_config(self):
        class Test(Configurable):
            config_items = [('test', True)]

        with self.assertRaises(ValueError):
            Test(config = {})

    def test_matching_config(self):
        class Test(Configurable):
            config_items = [('test', True)]

        t = Test(config = {'test': 'foobar'})
        self.assertEqual(t['test'], 'foobar')

    def test_extra_config(self):
        class Test(Configurable):
            config_items = [('test', True),
                            ('test2', False)]

        t = Test(config = {'test': 'foobar', 'test2': 'foo'})
        self.assertEqual(t['test'], 'foobar')
        self.assertEqual(t['test2'], 'foo')

    def test_default_config(self):
        class Test(Configurable):
            config_items = [('test', False),
                            ('test2', False),
                            ('test3', False)]

            def __init__(self, config, log=None):
                self['test2'] = 'foobar2'
                super(Test, self).__init__(config)

        t = Test(config = {'test': 'foobar'})
        self.assertEqual(t['test'], 'foobar')
        self.assertEqual(t['test2'], 'foobar2')
        self.assertIsNone(t['test3'])
