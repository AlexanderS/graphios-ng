import unittest
import graphios_ng.config

class ConfigItemTest(unittest.TestCase):
    def setUp(self):
        self.config = {'a': 1, 'b': 2, 'c': 3}
        self.item = graphios_ng.config.ConfigItem(self.config)
        self.multiple_items = graphios_ng.config.ConfigItem({'a': 17, 'b': self.item})

    def test_default_values(self):
        for (key, value) in self.config.items():
            self.assertEqual(getattr(self.item, key), value)

    def test_multiple_levels(self):
        self.assertEqual(self.multiple_items.a, 17)
        for (key, value) in self.config.items():
            self.assertEqual(getattr(self.multiple_items.b, key), value)

    def test_set_new_values(self):
        new_values = {'a': 23, 'b': 42}
        self.item.set(new_values)
        self.assertEqual(self.item.a, new_values['a'])
        self.assertEqual(self.item.b, new_values['b'])
        self.assertEqual(self.item.c, self.config['c'])

    def test_set_new_values_multiple_levels(self):
        new_values = {'a': 23, 'b': {'a': 42, 'b': 13}}
        self.multiple_items.set(new_values)
        self.assertEqual(self.multiple_items.a, new_values['a'])
        self.assertEqual(self.multiple_items.b.a, new_values['b']['a'])
        self.assertEqual(self.multiple_items.b.b, new_values['b']['b'])

    def test_keep_defaults(self):
        self.item.set({'a': 0, 'b': 0})
        self.assertEqual(self.item.c, self.config['c'])

    def test_keep_defaults_multiple_levels(self):
        new_values = {'a': 0, 'b': 0}
        self.multiple_items.b.set(new_values)

        for (key, value) in new_values.items():
            self.assertEqual(getattr(self.multiple_items.b, key), value)
        self.assertEqual(self.multiple_items.b.c, self.config['c'])

    def test_set_new_value(self):
        new_value = {'d': 123}
        self.item.set(new_value)
        self.assertEqual(self.item.d, new_value['d'])

    def test_set_new_value_multiple_levels(self):
        new_value = {'b': {'d': 123}}
        self.multiple_items.set(new_value)
        self.assertEqual(self.multiple_items.b.d, new_value['b']['d'])

    def test_set_new_value_multiple_levels(self):
        new_value = {'c': {'d': 123}}
        newer_value = {'c': {'f': 321}}
        self.multiple_items.set(new_value)
        self.assertEqual(self.multiple_items.c['d'], new_value['c']['d'])

        self.multiple_items.set(newer_value)
        self.assertEqual(self.multiple_items.c['f'], newer_value['c']['f'])
        self.assertFalse('d' in self.multiple_items.c)

