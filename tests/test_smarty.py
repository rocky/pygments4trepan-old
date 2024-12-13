# -*- coding: utf-8 -*-
"""
    Basic SmartyLexer Test
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2006-2014 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import unittest

from pygments.token import Operator, Number, Text, Token
from pygments.lexers import SmartyLexer


class SmartyTest(unittest.TestCase):

    def setUp(self):
        self.lexer = SmartyLexer()

    def testNestedCurly(self):
        fragment = '{templateFunction param={anotherFunction} param2=$something}\n'
        tokens = [
            (Token.Comment.Preproc, '{'),
            (Token.Name.Function, 'templateFunction'),
            (Token.Text, ' '),
            (Token.Name.Attribute, 'param'),
            (Token.Operator, '='),
            (Token.Comment.Preproc, '{'),
            (Token.Name.Attribute, 'anotherFunction'),
            (Token.Comment.Preproc, '}'),
            (Token.Text, ' '),
            (Token.Name.Attribute, 'param2'),
            (Token.Operator, '='),
            (Token.Name.Variable, '$something'),
            (Token.Comment.Preproc, '}'),
            (Token.Other, '\n'),
        ]
        self.assertEqual(tokens, list(self.lexer.get_tokens(fragment)))
