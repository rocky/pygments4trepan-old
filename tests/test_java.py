# -*- coding: utf-8 -*-
"""
    Basic JavaLexer Test
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2006-2014 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import unittest

from pygments.token import Text, Name, Operator, Keyword
from pygments.lexers import JavaLexer


class JavaTest(unittest.TestCase):

    def setUp(self):
        self.lexer = JavaLexer()
        self.maxDiff = None

    def testEnhancedFor(self):
        fragment = 'label:\nfor(String var2: var1) {}\n'
        tokens = [
            (Name.Label, 'label:'),
            (Text, '\n'),
            (Keyword, 'for'),
            (Operator, '('),
            (Name, 'String'),
            (Text, ' '),
            (Name, 'var2'),
            (Operator, ':'),
            (Text, ' '),
            (Name, 'var1'),
            (Operator, ')'),
            (Text, ' '),
            (Operator, '{'),
            (Operator, '}'),
            (Text, '\n'),
        ]
        self.assertEqual(tokens, list(self.lexer.get_tokens(fragment)))
