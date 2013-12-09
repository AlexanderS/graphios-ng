import os
import shutil
import tempfile
import unittest

from graphios_ng.output.extinfo import ExtinfoOutput


class ExtinfoOutputTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.mkdtemp()
        config = {'dir': self.directory,
                  'filename': 'foo/{host}/{service}/host-{host}-service-{service}.cfg',
                  'template': '''
define serviceextinfo {{
    host_name            {host}
    service_description  {service}
}}
'''}
        self.output = ExtinfoOutput(config)
        self.elem = {'host': 'test', 'service': 'te / st2'}
        self.expected_path = os.path.join(
            self.directory, 'foo', 'test', 'te__st2',
            'host-test-service-te__st2.cfg')

    def tearDown(self):
        shutil.rmtree(self.directory)

    def test_content(self):
        content = self.output._build_content(self.elem)
        self.assertEquals(content, '''
define serviceextinfo {
    host_name            test
    service_description  te / st2
}
''')

    def test_path(self):
        path = self.output._build_path(self.elem)
        self.assertEquals(path, self.expected_path)

    def test_create_directory(self):
        path = self.output._build_path(self.elem)
        directory = os.path.join(self.directory, 'foo')
        self.assertFalse(os.path.exists(directory))
        self.output._create_directory(path)
        self.assertTrue(os.path.exists(directory))

    def test_count_elem(self):
        self.count = 0
        def count(elem):
            self.count += 1
            self.assertEquals(elem['host'], 'test%d' % self.count)
            self.assertEquals(elem['service'], '%dte / st2' % self.count)

        self.output._handle_elem = count

        data = [
            {'host': 'test1', 'service': '1te / st2'},
            {'host': 'test2', 'service': '2te / st2'},
            {'host': 'test3', 'service': '3te / st2'},
            {'host': 'test4', 'service': '4te / st2'}
            ]
        self.output.output(data)
        self.assertEquals(self.count, len(data))

    def test_handle_elem(self):
        self.assertFalse(os.path.exists(self.expected_path))
        self.output._handle_elem(self.elem)
        self.assertTrue(os.path.exists(self.expected_path))
        with open(self.expected_path, 'r') as outputfile:
            content = outputfile.read()
            self.assertEquals(content, '''
define serviceextinfo {
    host_name            test
    service_description  te / st2
}
''')
