import unittest

from graphios_ng.parser.json_line import JsonLineParser


class JsonLineParserTest(unittest.TestCase):
    def setUp(self):
        config = {'path': ''}
        self.parser = JsonLineParser(config, None)

    def test_incomplete_json_data(self):
        with self.assertRaises(ValueError):
            self.parser._parse_host_perfline("{'data': 'test', 'fo")
