# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
from graphios_ng import utils


class WithLogTest(unittest.TestCase):
    def test_with_log(self):
        @utils.with_log
        def testing(log=None):
            self.assertIsNotNone(log)
            self.assertEquals(str(type(log)), "<class 'logging.Logger'>")
        testing()

    def test_with_log_overwrite(self):
        @utils.with_log
        def testing(log=None):
            self.assertEquals(log, 'Should not change')
        testing(log = 'Should not change')


class TemplateTest(unittest.TestCase):
    def test_querystring(self):
        t = utils.Template('${query|urlencode}')
        self.assertEquals(
            t.substitute(query='string_of_characters_like_these:$#@=?%^Q^$'),
            'string_of_characters_like_these%3A%24%23%40%3D%3F%25%5EQ%5E%24')

    def test_filename(self):
        t = utils.Template('${file|filename}')
        self.assertEquals(
            t.substitute(file='foobar / test äöüß blub\'s'),
            'foobar__test_äöüß_blubs')
