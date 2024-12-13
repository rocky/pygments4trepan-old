# -*- coding: utf-8 -*-
"""
    Basic CLexer Test
    ~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2006-2014 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import unittest
import os
import textwrap

from pygments.token import Text, Number, Token
from pygments.lexers import CLexer


class CLexerTest(unittest.TestCase):

    def setUp(self):
        self.lexer = CLexer()

    def testNumbers(self):
        code = '42 23.42 23. .42 023 0xdeadbeef 23e+42 42e-23'
        wanted = []
        for item in zip([Number.Integer, Number.Float, Number.Float,
                         Number.Float, Number.Oct, Number.Hex,
                         Number.Float, Number.Float], code.split()):
            wanted.append(item)
            wanted.append((Text, ' '))
        wanted = wanted[:-1] + [(Text, '\n')]
        self.assertEqual(list(self.lexer.get_tokens(code)), wanted)

    def testSwitch(self):
        fragment = '''\
        int main()
        {
            switch (0)
            {
                case 0:
                default:
                    ;
            }
        }
        '''
        tokens = [
            (Token.Keyword.Type, 'int'),
            (Token.Text, ' '),
            (Token.Name.Function, 'main'),
            (Token.Punctuation, '('),
            (Token.Punctuation, ')'),
            (Token.Text, '\n'),
            (Token.Punctuation, '{'),
            (Token.Text, '\n'),
            (Token.Text, '    '),
            (Token.Keyword, 'switch'),
            (Token.Text, ' '),
            (Token.Punctuation, '('),
            (Token.Literal.Number.Integer, '0'),
            (Token.Punctuation, ')'),
            (Token.Text, '\n'),
            (Token.Text, '    '),
            (Token.Punctuation, '{'),
            (Token.Text, '\n'),
            (Token.Text, '        '),
            (Token.Keyword, 'case'),
            (Token.Text, ' '),
            (Token.Literal.Number.Integer, '0'),
            (Token.Operator, ':'),
            (Token.Text, '\n'),
            (Token.Text, '        '),
            (Token.Keyword, 'default'),
            (Token.Operator, ':'),
            (Token.Text, '\n'),
            (Token.Text, '            '),
            (Token.Punctuation, ';'),
            (Token.Text, '\n'),
            (Token.Text, '    '),
            (Token.Punctuation, '}'),
            (Token.Text, '\n'),
            (Token.Punctuation, '}'),
            (Token.Text, '\n'),
        ]
        self.assertEqual(tokens, list(self.lexer.get_tokens(textwrap.dedent(fragment))))

    def testSwitchSpaceBeforeColon(self):
        fragment = '''\
        int main()
        {
            switch (0)
            {
                case 0 :
                default :
                    ;
            }
        }
        '''
        tokens = [
            (Token.Keyword.Type, 'int'),
            (Token.Text, ' '),
            (Token.Name.Function, 'main'),
            (Token.Punctuation, '('),
            (Token.Punctuation, ')'),
            (Token.Text, '\n'),
            (Token.Punctuation, '{'),
            (Token.Text, '\n'),
            (Token.Text, '    '),
            (Token.Keyword, 'switch'),
            (Token.Text, ' '),
            (Token.Punctuation, '('),
            (Token.Literal.Number.Integer, '0'),
            (Token.Punctuation, ')'),
            (Token.Text, '\n'),
            (Token.Text, '    '),
            (Token.Punctuation, '{'),
            (Token.Text, '\n'),
            (Token.Text, '        '),
            (Token.Keyword, 'case'),
            (Token.Text, ' '),
            (Token.Literal.Number.Integer, '0'),
            (Token.Text, ' '),
            (Token.Operator, ':'),
            (Token.Text, '\n'),
            (Token.Text, '        '),
            (Token.Keyword, 'default'),
            (Token.Text, ' '),
            (Token.Operator, ':'),
            (Token.Text, '\n'),
            (Token.Text, '            '),
            (Token.Punctuation, ';'),
            (Token.Text, '\n'),
            (Token.Text, '    '),
            (Token.Punctuation, '}'),
            (Token.Text, '\n'),
            (Token.Punctuation, '}'),
            (Token.Text, '\n'),
        ]
        self.assertEqual(tokens, list(self.lexer.get_tokens(textwrap.dedent(fragment))))

    def testLabel(self):
        fragment = '''\
        int main()
        {
        foo:
          goto foo;
        }
        '''
        tokens = [
            (Token.Keyword.Type, 'int'),
            (Token.Text, ' '),
            (Token.Name.Function, 'main'),
            (Token.Punctuation, '('),
            (Token.Punctuation, ')'),
            (Token.Text, '\n'),
            (Token.Punctuation, '{'),
            (Token.Text, '\n'),
            (Token.Name.Label, 'foo'),
            (Token.Punctuation, ':'),
            (Token.Text, '\n'),
            (Token.Text, '  '),
            (Token.Keyword, 'goto'),
            (Token.Text, ' '),
            (Token.Name, 'foo'),
            (Token.Punctuation, ';'),
            (Token.Text, '\n'),
            (Token.Punctuation, '}'),
            (Token.Text, '\n'),
        ]
        self.assertEqual(tokens, list(self.lexer.get_tokens(textwrap.dedent(fragment))))

    def testLabelSpaceBeforeColon(self):
        fragment = '''\
        int main()
        {
        foo :
          goto foo;
        }
        '''
        tokens = [
            (Token.Keyword.Type, 'int'),
            (Token.Text, ' '),
            (Token.Name.Function, 'main'),
            (Token.Punctuation, '('),
            (Token.Punctuation, ')'),
            (Token.Text, '\n'),
            (Token.Punctuation, '{'),
            (Token.Text, '\n'),
            (Token.Name.Label, 'foo'),
            (Token.Text, ' '),
            (Token.Punctuation, ':'),
            (Token.Text, '\n'),
            (Token.Text, '  '),
            (Token.Keyword, 'goto'),
            (Token.Text, ' '),
            (Token.Name, 'foo'),
            (Token.Punctuation, ';'),
            (Token.Text, '\n'),
            (Token.Punctuation, '}'),
            (Token.Text, '\n'),
        ]
        self.assertEqual(tokens, list(self.lexer.get_tokens(textwrap.dedent(fragment))))

    def testLabelFollowedByStatement(self):
        fragment = '''\
        int main()
        {
        foo:return 0;
          goto foo;
        }
        '''
        tokens = [
            (Token.Keyword.Type, 'int'),
            (Token.Text, ' '),
            (Token.Name.Function, 'main'),
            (Token.Punctuation, '('),
            (Token.Punctuation, ')'),
            (Token.Text, '\n'),
            (Token.Punctuation, '{'),
            (Token.Text, '\n'),
            (Token.Name.Label, 'foo'),
            (Token.Punctuation, ':'),
            (Token.Keyword, 'return'),
            (Token.Text, ' '),
            (Token.Literal.Number.Integer, '0'),
            (Token.Punctuation, ';'),
            (Token.Text, '\n'),
            (Token.Text, '  '),
            (Token.Keyword, 'goto'),
            (Token.Text, ' '),
            (Token.Name, 'foo'),
            (Token.Punctuation, ';'),
            (Token.Text, '\n'),
            (Token.Punctuation, '}'),
            (Token.Text, '\n'),
        ]
        self.assertEqual(tokens, list(self.lexer.get_tokens(textwrap.dedent(fragment))))
