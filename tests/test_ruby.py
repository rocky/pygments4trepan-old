# -*- coding: utf-8 -*-
"""
    Basic RubyLexer Test
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2006-2014 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import unittest

from pygments.token import Operator, Number, Text, Token
from pygments.lexers import RubyLexer


class RubyTest(unittest.TestCase):

    def setUp(self):
        self.lexer = RubyLexer()
        self.maxDiff = None

    def testRangeSyntax1(self):
        fragment = '1..3\n'
        tokens = [
            (Number.Integer, '1'),
            (Operator, '..'),
            (Number.Integer, '3'),
            (Text, '\n'),
        ]
        self.assertEqual(tokens, list(self.lexer.get_tokens(fragment)))

    def testRangeSyntax2(self):
        fragment = '1...3\n'
        tokens = [
            (Number.Integer, '1'),
            (Operator, '...'),
            (Number.Integer, '3'),
            (Text, '\n'),
        ]
        self.assertEqual(tokens, list(self.lexer.get_tokens(fragment)))

    def testRangeSyntax3(self):
        fragment = '1 .. 3\n'
        tokens = [
            (Number.Integer, '1'),
            (Text, ' '),
            (Operator, '..'),
            (Text, ' '),
            (Number.Integer, '3'),
            (Text, '\n'),
        ]
        self.assertEqual(tokens, list(self.lexer.get_tokens(fragment)))

    def testInterpolationNestedCurly(self):
        fragment = (
            '"A#{ (3..5).group_by { |x| x/2}.map '
            'do |k,v| "#{k}" end.join }" + "Z"\n')

        tokens = [
            (Token.Literal.String.Double, '"'),
            (Token.Literal.String.Double, 'A'),
            (Token.Literal.String.Interpol, '#{'),
            (Token.Text, ' '),
            (Token.Punctuation, '('),
            (Token.Literal.Number.Integer, '3'),
            (Token.Operator, '..'),
            (Token.Literal.Number.Integer, '5'),
            (Token.Punctuation, ')'),
            (Token.Operator, '.'),
            (Token.Name, 'group_by'),
            (Token.Text, ' '),
            (Token.Literal.String.Interpol, '{'),
            (Token.Text, ' '),
            (Token.Operator, '|'),
            (Token.Name, 'x'),
            (Token.Operator, '|'),
            (Token.Text, ' '),
            (Token.Name, 'x'),
            (Token.Operator, '/'),
            (Token.Literal.Number.Integer, '2'),
            (Token.Literal.String.Interpol, '}'),
            (Token.Operator, '.'),
            (Token.Name, 'map'),
            (Token.Text, ' '),
            (Token.Keyword, 'do'),
            (Token.Text, ' '),
            (Token.Operator, '|'),
            (Token.Name, 'k'),
            (Token.Punctuation, ','),
            (Token.Name, 'v'),
            (Token.Operator, '|'),
            (Token.Text, ' '),
            (Token.Literal.String.Double, '"'),
            (Token.Literal.String.Interpol, '#{'),
            (Token.Name, 'k'),
            (Token.Literal.String.Interpol, '}'),
            (Token.Literal.String.Double, '"'),
            (Token.Text, ' '),
            (Token.Keyword, 'end'),
            (Token.Operator, '.'),
            (Token.Name, 'join'),
            (Token.Text, ' '),
            (Token.Literal.String.Interpol, '}'),
            (Token.Literal.String.Double, '"'),
            (Token.Text, ' '),
            (Token.Operator, '+'),
            (Token.Text, ' '),
            (Token.Literal.String.Double, '"'),
            (Token.Literal.String.Double, 'Z'),
            (Token.Literal.String.Double, '"'),
            (Token.Text, '\n'),
        ]
        self.assertEqual(tokens, list(self.lexer.get_tokens(fragment)))

    def testOperatorMethods(self):
        fragment = 'x.==4\n'
        tokens = [
            (Token.Name, 'x'),
            (Token.Operator, '.'),
            (Token.Name.Operator, '=='),
            (Token.Literal.Number.Integer, '4'),
            (Token.Text, '\n'),
        ]
        self.assertEqual(tokens, list(self.lexer.get_tokens(fragment)))

    def testEscapedBracestring(self):
        fragment = 'str.gsub(%r{\\\\\\\\}, "/")\n'
        tokens = [
            (Token.Name, 'str'),
            (Token.Operator, '.'),
            (Token.Name, 'gsub'),
            (Token.Punctuation, '('),
            (Token.Literal.String.Regex, '%r{'),
            (Token.Literal.String.Regex, '\\\\'),
            (Token.Literal.String.Regex, '\\\\'),
            (Token.Literal.String.Regex, '}'),
            (Token.Punctuation, ','),
            (Token.Text, ' '),
            (Token.Literal.String.Double, '"'),
            (Token.Literal.String.Double, '/'),
            (Token.Literal.String.Double, '"'),
            (Token.Punctuation, ')'),
            (Token.Text, '\n'),
        ]
        self.assertEqual(tokens, list(self.lexer.get_tokens(fragment)))
