# -*- coding: utf-8 -*-
"""
    Basic Shell Tests
    ~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2006-2014 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import unittest

from pygments.token import Token
from pygments.lexers import BashLexer


class BashTest(unittest.TestCase):

    def setUp(self):
        self.lexer = BashLexer()
        self.maxDiff = None

    def testCurlyNoEscapeAndQuotes(self):
        fragment = 'echo "${a//["b"]/}"\n'
        tokens = [
            (Token.Name.Builtin, 'echo'),
            (Token.Text, ' '),
            (Token.Literal.String.Double, '"'),
            (Token.String.Interpol, '${'),
            (Token.Name.Variable, 'a'),
            (Token.Punctuation, '//['),
            (Token.Literal.String.Double, '"b"'),
            (Token.Punctuation, ']/'),
            (Token.String.Interpol, '}'),
            (Token.Literal.String.Double, '"'),
            (Token.Text, '\n'),
        ]
        self.assertEqual(tokens, list(self.lexer.get_tokens(fragment)))

    def testCurlyWithEscape(self):
        fragment = 'echo ${a//[\\"]/}\n'
        tokens = [
            (Token.Name.Builtin, 'echo'),
            (Token.Text, ' '),
            (Token.String.Interpol, '${'),
            (Token.Name.Variable, 'a'),
            (Token.Punctuation, '//['),
            (Token.Literal.String.Escape, '\\"'),
            (Token.Punctuation, ']/'),
            (Token.String.Interpol, '}'),
            (Token.Text, '\n'),
        ]
        self.assertEqual(tokens, list(self.lexer.get_tokens(fragment)))

    def testParsedSingle(self):
        fragment = "a=$'abc\\''\n"
        tokens = [
            (Token.Name.Variable, 'a'),
            (Token.Operator, '='),
            (Token.Literal.String.Single, "$'abc\\''"),
            (Token.Text, '\n'),
        ]
        self.assertEqual(tokens, list(self.lexer.get_tokens(fragment)))
