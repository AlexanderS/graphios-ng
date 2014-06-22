import unittest

from graphios_ng import output


class OuputTest(unittest.TestCase):
    def test_invalid_output_type(self):
        config = {'type': 'invalid'}
        out = output.create_output(config)
        self.assertIsNone(out)

    def test_missing_output_type(self):
        config = {}
        out = output.create_output(config)
        self.assertIsNone(out)

    def test_extinfo_output_type(self):
        config = {'type': 'extinfo', 'dir': None, 'filename': None}
        out = output.create_output(config)
        self.assertIsNotNone(out)
        self.assertEqual(str(type(out)), "<class 'graphios_ng.output.extinfo.ExtinfoOutput'>")

    def test_carbon_output_type(self):
        config = {'type': 'carbon'}
        out = output.create_output(config)
        self.assertIsNotNone(out)
        self.assertEqual(str(type(out)), "<class 'graphios_ng.output.carbon.CarbonOutput'>")

    def test_ngraph_output_type(self):
        config = {'type': 'ngraph'}
        out = output.create_output(config)
        self.assertIsNotNone(out)
        self.assertEqual(str(type(out)), "<class 'graphios_ng.output.ngraph.NgraphOutput'>")

    def test_output_config(self):
        config = {'type': 'extinfo','filename': None}
        out = output.create_output(config)
        self.assertIsNotNone(out)
        self.assertEqual(out.config['filename'], None)

    def test_missing_config(self):
        config = {'type': 'extinfo'}
        config2 = {'type': 'extinfo', 'dir': None}
        with self.assertRaises(ValueError):
            output.create_output(config)

        with self.assertRaises(ValueError):
            output.create_output(config2)
