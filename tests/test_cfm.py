# -*- coding: utf-8 -*-
"""
    Basic ColdfusionHtmlLexer Test
    ~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import unittest
import os

from pygments.token import Token
from pygments.lexers import ColdfusionHtmlLexer


class ColdfusionHtmlLexerTest(unittest.TestCase):

    def setUp(self):
        self.lexer = ColdfusionHtmlLexer()

    def testBasicComment(self):
        fragment = '<!--- cfcomment --->'
        expected = [
            (Token.Text, ''),
            (Token.Comment.Multiline, '<!---'),
            (Token.Comment.Multiline, ' cfcomment '),
            (Token.Comment.Multiline, '--->'),
            (Token.Text, '\n'),
        ]
        self.assertEqual(expected, list(self.lexer.get_tokens(fragment)))

    def testNestedComment(self):
        fragment = '<!--- nested <!--- cfcomment ---> --->'
        expected = [
            (Token.Text, ''),
            (Token.Comment.Multiline, '<!---'),
            (Token.Comment.Multiline, ' nested '),
            (Token.Comment.Multiline, '<!---'),
            (Token.Comment.Multiline, ' cfcomment '),
            (Token.Comment.Multiline, '--->'),
            (Token.Comment.Multiline, ' '),
            (Token.Comment.Multiline, '--->'),
            (Token.Text, '\n'),
        ]
        self.assertEqual(expected, list(self.lexer.get_tokens(fragment)))
