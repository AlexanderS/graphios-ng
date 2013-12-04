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
        config = {'type': 'extinfo'}
        out = output.create_output(config)
        self.assertIsNotNone(out)
        self.assertEquals(str(type(out)), "<class 'graphios_ng.output.extinfo.ExtinfoOutput'>")

    def test_carbon_output_type(self):
        config = {'type': 'carbon'}
        out = output.create_output(config)
        self.assertIsNotNone(out)
        self.assertEquals(str(type(out)), "<class 'graphios_ng.output.carbon.CarbonOutput'>")

    def test_ngraph_output_type(self):
        config = {'type': 'ngraph'}
        out = output.create_output(config)
        self.assertIsNotNone(out)
        self.assertEquals(str(type(out)), "<class 'graphios_ng.output.ngraph.NgraphOutput'>")

    def test_output_config(self):
        config = {'type': 'extinfo', 'foobar': 123}
        out = output.create_output(config)
        self.assertIsNotNone(out)
        self.assertEquals(out.config['foobar'], 123)
