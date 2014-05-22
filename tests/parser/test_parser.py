import unittest

from graphios_ng import parser


class ParserTest(unittest.TestCase):
    def test_invalid_parser_type(self):
        config = {'type': 'invalid'}
        p = parser.create_parser(config)
        self.assertIsNone(p)

    def test_missing_parser_type(self):
        config = {}
        p = parser.create_parser(config)
        self.assertIsNone(p)

    def test_json_line_parser_type(self):
        config = {'type': 'json_line'}
        p = parser.create_parser(config)
        self.assertIsNotNone(p)
        self.assertEqual(str(type(p)), "<class 'graphios_ng.parser.json_line.JsonLineParser'>")

    def test_ngraph_parser_type(self):
        config = {'type': 'ngraph'}
        p = parser.create_parser(config)
        self.assertIsNotNone(p)
        self.assertEqual(str(type(p)), "<class 'graphios_ng.parser.ngraph.NgraphParser'>")

    def test_pnp4nagios_parser_type(self):
        config = {'type': 'pnp4nagios'}
        p = parser.create_parser(config)
        self.assertIsNotNone(p)
        self.assertEqual(str(type(p)), "<class 'graphios_ng.parser.pnp4nagios.Pnp4nagiosParser'>")
