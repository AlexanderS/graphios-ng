import unittest
from graphios_ng.configurable import ConfigItem, Configurable


class ConfigurableTest(unittest.TestCase):
    def test_missing_config(self):
        class Test(Configurable):
            config_items = [ConfigItem('test', required=True)]

        with self.assertRaises(ValueError):
            Test(config = {})

    def test_matching_config(self):
        class Test(Configurable):
            config_items = [ConfigItem('test', required=True)]

        t = Test(config = {'test': 'foobar'})
        self.assertEqual(t.config['test'], 'foobar')

    def test_extra_config(self):
        class Test(Configurable):
            config_items = [ConfigItem('test', required=True),
                            ConfigItem('test2')]

        t = Test(config = {'test': 'foobar', 'test2': 'foo'})
        self.assertEqual(t.config['test'], 'foobar')
        self.assertEqual(t.config['test2'], 'foo')

    def test_default_config(self):
        class Test(Configurable):
            config_items = [ConfigItem('test'),
                            ConfigItem('test2', default='foobar2'),
                            ConfigItem('test3')]

        t = Test(config = {'test': 'foobar'})
        self.assertEqual(t.config['test'], 'foobar')
        self.assertEqual(t.config['test2'], 'foobar2')
        self.assertIsNone(t.config['test3'])
