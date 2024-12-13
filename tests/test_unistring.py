# -*- coding: utf-8 -*-
"""
    Test suite for the unistring module
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2006-2014 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
import unittest
import random

from pygments import unistring as uni
from pygments.util import unichr


class UnistringTest(unittest.TestCase):
    def test_cats_exist_and_compilable(self):
        for cat in uni.cats:
            if not hasattr(uni, cat):
                continue
            s = getattr(uni, cat)
            if s == '':  # Probably Cs on Jython
                continue
            print("%s %r" % (cat, s))
            re.compile('[%s]' % s)

    def _cats_that_match(self, c):
        matching_cats = []
        for cat in uni.cats:
            if not hasattr(uni, cat):
                continue
            s = getattr(uni, cat)
            if s == '':  # Probably Cs on Jython
                continue
            if re.compile('[%s]' % s).match(c):
                matching_cats.append(cat)
        return matching_cats
