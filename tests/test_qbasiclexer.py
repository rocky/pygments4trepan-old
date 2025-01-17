# -*- coding: utf-8 -*-
"""
    Tests for QBasic
    ~~~~~~~~~~~~~~~~

    :copyright: Copyright 2006-2014 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import glob
import os
import unittest

from pygments.token import Token
from pygments.lexers.basic import QBasicLexer


class QBasicTest(unittest.TestCase):
    def setUp(self):
        self.lexer = QBasicLexer()
        self.maxDiff = None

    def testKeywordsWithDollar(self):
        fragment = 'DIM x\nx = RIGHT$("abc", 1)\n'
        expected = [
            (Token.Keyword.Declaration, 'DIM'),
            (Token.Text.Whitespace, ' '),
            (Token.Name.Variable.Global, 'x'),
            (Token.Text, '\n'),
            (Token.Name.Variable.Global, 'x'),
            (Token.Text.Whitespace, ' '),
            (Token.Operator, '='),
            (Token.Text.Whitespace, ' '),
            (Token.Keyword.Reserved, 'RIGHT$'),
            (Token.Punctuation, '('),
            (Token.Literal.String.Double, '"abc"'),
            (Token.Punctuation, ','),
            (Token.Text.Whitespace, ' '),
            (Token.Literal.Number.Integer.Long, '1'),
            (Token.Punctuation, ')'),
            (Token.Text, '\n'),
        ]
        self.assertEqual(expected, list(self.lexer.get_tokens(fragment)))
