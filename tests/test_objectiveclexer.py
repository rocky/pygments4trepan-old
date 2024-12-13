# -*- coding: utf-8 -*-
"""
    Basic CLexer Test
    ~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2006-2014 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import unittest
import os

from pygments.token import Token
from pygments.lexers import ObjectiveCLexer


class ObjectiveCLexerTest(unittest.TestCase):

    def setUp(self):
        self.lexer = ObjectiveCLexer()

    def testLiteralNumberInt(self):
        fragment = '@(1);\n'
        expected = [
            (Token.Literal, '@('),
            (Token.Literal.Number.Integer, '1'),
            (Token.Literal, ')'),
            (Token.Punctuation, ';'),
            (Token.Text, '\n'),
        ]
        self.assertEqual(expected, list(self.lexer.get_tokens(fragment)))

    def testLiteralNumberExpression(self):
        fragment = '@(1+2);\n'
        expected = [
            (Token.Literal, '@('),
            (Token.Literal.Number.Integer, '1'),
            (Token.Operator, '+'),
            (Token.Literal.Number.Integer, '2'),
            (Token.Literal, ')'),
            (Token.Punctuation, ';'),
            (Token.Text, '\n'),
        ]
        self.assertEqual(expected, list(self.lexer.get_tokens(fragment)))

    def testLiteralNumberNestedExpression(self):
        fragment = '@(1+(2+3));\n'
        expected = [
            (Token.Literal, '@('),
            (Token.Literal.Number.Integer, '1'),
            (Token.Operator, '+'),
            (Token.Punctuation, '('),
            (Token.Literal.Number.Integer, '2'),
            (Token.Operator, '+'),
            (Token.Literal.Number.Integer, '3'),
            (Token.Punctuation, ')'),
            (Token.Literal, ')'),
            (Token.Punctuation, ';'),
            (Token.Text, '\n'),
        ]
        self.assertEqual(expected, list(self.lexer.get_tokens(fragment)))

    def testLiteralNumberBool(self):
        fragment = '@NO;\n'
        expected = [
            (Token.Literal.Number, '@NO'),
            (Token.Punctuation, ';'),
            (Token.Text, '\n'),
        ]
        self.assertEqual(expected, list(self.lexer.get_tokens(fragment)))

    def testLieralNumberBoolExpression(self):
        fragment = '@(YES);\n'
        expected = [
            (Token.Literal, '@('),
            (Token.Name.Builtin, 'YES'),
            (Token.Literal, ')'),
            (Token.Punctuation, ';'),
            (Token.Text, '\n'),
        ]
        self.assertEqual(expected, list(self.lexer.get_tokens(fragment)))
