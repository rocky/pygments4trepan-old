# -*- coding: utf-8 -*-
"""
    pygments.lexers.templates
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for various template engines' markup.

    :copyright: Copyright 2006-2014 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from pygments.lexers.html import XmlLexer
from pygments.lexers.css import CssLexer
from pygments.lexers.php import PhpLexer
from pygments.lexers.python import PythonLexer
from pygments.lexers.data import YamlLexer
from pygments.lexer import Lexer, DelegatingLexer, RegexLexer, bygroups, \
    include, using, this, default, combined
from pygments.token import Error, Punctuation, Whitespace, \
    Text, Comment, Operator, Keyword, Name, String, Number, Other, Token
from pygments.util import html_doctype_matches, looks_like_xml

__all__ = ['XmlPhpLexer', 'CssPhpLexer',
           'JavascriptPhpLexer',
           'XmlErbLexer', 'CssErbLexer',
           'XmlSmartyLexer',
           'CssSmartyLexer', 'JavascriptSmartyLexer', 'DjangoLexer',
           'CssDjangoLexer', 'XmlDjangoLexer',
           'JavascriptDjangoLexer', 'GenshiLexer',
           'GenshiTextLexer', 'CssGenshiLexer', 'JavascriptGenshiLexer',
           'MyghtyLexer', 'MyghtyXmlLexer',
           'MyghtyCssLexer', 'MakoLexer',
           'MakoHtmlLexer', 'MakoXmlLexer', 'MakoJavascriptLexer',
           'MakoCssLexer', 'CheetahLexer',
           'EvoqueLexer',
           'EvoqueXmlLexer', 'ColdfusionLexer',
           'ColdfusionCFCLexer', 'VelocityLexer',
           'VelocityHtmlLexer', 'VelocityXmlLexer',
           'LassoHtmlLexer', 'LassoXmlLexer',
           'LassoCssLexer', 'LassoJavascriptLexer', 'HandlebarsLexer',
           'YamlJinjaLexer', 'LiquidLexer',
           'TwigLexer', 'TwigHtmlLexer']


class SmartyLexer(RegexLexer):
    """
    Generic `Smarty <http://smarty.php.net/>`_ template lexer.

    Just highlights smarty code between the preprocessor directives, other
    data is left untouched by the lexer.
    """

    name = 'Smarty'
    aliases = ['smarty']
    filenames = ['*.tpl']
    mimetypes = ['application/x-smarty']

    flags = re.MULTILINE | re.DOTALL

    tokens = {
        'root': [
            (r'[^{]+', Other),
            (r'(\{)(\*.*?\*)(\})',
             bygroups(Comment.Preproc, Comment, Comment.Preproc)),
            (r'(\{php\})(.*?)(\{/php\})',
             bygroups(Comment.Preproc, using(PhpLexer, startinline=True),
                      Comment.Preproc)),
            (r'(\{)(/?[a-zA-Z_]\w*)(\s*)',
             bygroups(Comment.Preproc, Name.Function, Text), 'smarty'),
            (r'\{', Comment.Preproc, 'smarty')
        ],
        'smarty': [
            (r'\s+', Text),
            (r'\{', Comment.Preproc, '#push'),
            (r'\}', Comment.Preproc, '#pop'),
            (r'#[a-zA-Z_]\w*#', Name.Variable),
            (r'\$[a-zA-Z_]\w*(\.\w+)*', Name.Variable),
            (r'[~!%^&*()+=|\[\]:;,.<>/?@-]', Operator),
            (r'(true|false|null)\b', Keyword.Constant),
            (r"[0-9](\.[0-9]*)?(eE[+-][0-9])?[flFLdD]?|"
             r"0[xX][0-9a-fA-F]+[Ll]?", Number),
            (r'"(\\\\|\\"|[^"])*"', String.Double),
            (r"'(\\\\|\\'|[^'])*'", String.Single),
            (r'[a-zA-Z_]\w*', Name.Attribute)
        ]
    }

    def analyse_text(text):
        rv = 0.0
        if re.search(r'\{if\s+.*?\}.*?\{/if\}', text):
            rv += 0.15
        if re.search(r'\{include\s+file=.*?\}', text):
            rv += 0.15
        if re.search(r'\{foreach\s+.*?\}.*?\{/foreach\}', text):
            rv += 0.15
        if re.search(r'\{\$.*?\}', text):
            rv += 0.01
        return rv


class VelocityLexer(RegexLexer):
    """
    Generic `Velocity <http://velocity.apache.org/>`_ template lexer.

    Just highlights velocity directives and variable references, other
    data is left untouched by the lexer.
    """

    name = 'Velocity'
    aliases = ['velocity']
    filenames = ['*.vm', '*.fhtml']

    flags = re.MULTILINE | re.DOTALL

    identifier = r'[a-zA-Z_]\w*'

    tokens = {
        'root': [
            (r'[^{#$]+', Other),
            (r'(#)(\*.*?\*)(#)',
             bygroups(Comment.Preproc, Comment, Comment.Preproc)),
            (r'(##)(.*?$)',
             bygroups(Comment.Preproc, Comment)),
            (r'(#\{?)(' + identifier + r')(\}?)(\s?\()',
             bygroups(Comment.Preproc, Name.Function, Comment.Preproc, Punctuation),
             'directiveparams'),
            (r'(#\{?)(' + identifier + r')(\}|\b)',
             bygroups(Comment.Preproc, Name.Function, Comment.Preproc)),
            (r'\$\{?', Punctuation, 'variable')
        ],
        'variable': [
            (identifier, Name.Variable),
            (r'\(', Punctuation, 'funcparams'),
            (r'(\.)(' + identifier + r')',
             bygroups(Punctuation, Name.Variable), '#push'),
            (r'\}', Punctuation, '#pop'),
            default('#pop')
        ],
        'directiveparams': [
            (r'(&&|\|\||==?|!=?|[-<>+*%&|^/])|\b(eq|ne|gt|lt|ge|le|not|in)\b',
             Operator),
            (r'\[', Operator, 'rangeoperator'),
            (r'\b' + identifier + r'\b', Name.Function),
            include('funcparams')
        ],
        'rangeoperator': [
            (r'\.\.', Operator),
            include('funcparams'),
            (r'\]', Operator, '#pop')
        ],
        'funcparams': [
            (r'\$\{?', Punctuation, 'variable'),
            (r'\s+', Text),
            (r',', Punctuation),
            (r'"(\\\\|\\"|[^"])*"', String.Double),
            (r"'(\\\\|\\'|[^'])*'", String.Single),
            (r"0[xX][0-9a-fA-F]+[Ll]?", Number),
            (r"\b[0-9]+\b", Number),
            (r'(true|false|null)\b', Keyword.Constant),
            (r'\(', Punctuation, '#push'),
            (r'\)', Punctuation, '#pop'),
            (r'\[', Punctuation, '#push'),
            (r'\]', Punctuation, '#pop'),
        ]
    }

    def analyse_text(text):
        rv = 0.0
        if re.search(r'#\{?macro\}?\(.*?\).*?#\{?end\}?', text):
            rv += 0.25
        if re.search(r'#\{?if\}?\(.+?\).*?#\{?end\}?', text):
            rv += 0.15
        if re.search(r'#\{?foreach\}?\(.+?\).*?#\{?end\}?', text):
            rv += 0.15
        if re.search(r'\$\{?[a-zA-Z_]\w*(\([^)]*\))?'
                     r'(\.\w+(\([^)]*\))?)*\}?', text):
            rv += 0.01
        return rv


class VelocityHtmlLexer(DelegatingLexer):
    """
    Subclass of the `VelocityLexer` that highlights unlexed data
    with the `HtmlLexer`.

    """

    name = 'HTML+Velocity'
    aliases = ['html+velocity']
    alias_filenames = ['*.html', '*.fhtml']
    mimetypes = ['text/html+velocity']

    def __init__(self, **options):
        super(VelocityHtmlLexer, self).__init__(VelocityLexer,
                                                **options)


class VelocityXmlLexer(DelegatingLexer):
    """
    Subclass of the `VelocityLexer` that highlights unlexed data
    with the `XmlLexer`.

    """

    name = 'XML+Velocity'
    aliases = ['xml+velocity']
    alias_filenames = ['*.xml', '*.vm']
    mimetypes = ['application/xml+velocity']

    def __init__(self, **options):
        super(VelocityXmlLexer, self).__init__(XmlLexer, VelocityLexer,
                                               **options)

    def analyse_text(text):
        rv = VelocityLexer.analyse_text(text) - 0.01
        if looks_like_xml(text):
            rv += 0.4
        return rv


class DjangoLexer(RegexLexer):
    """
    Generic `django <http://www.djangoproject.com/documentation/templates/>`_
    and `jinja <http://wsgiarea.pocoo.org/jinja/>`_ template lexer.

    It just highlights django/jinja code between the preprocessor directives,
    other data is left untouched by the lexer.
    """

    name = 'Django/Jinja'
    aliases = ['django', 'jinja']
    mimetypes = ['application/x-django-templating', 'application/x-jinja']

    flags = re.M | re.S

    tokens = {
        'root': [
            (r'[^{]+', Other),
            (r'\{\{', Comment.Preproc, 'var'),
            # jinja/django comments
            (r'\{[*#].*?[*#]\}', Comment),
            # django comments
            (r'(\{%)(-?\s*)(comment)(\s*-?)(%\})(.*?)'
             r'(\{%)(-?\s*)(endcomment)(\s*-?)(%\})',
             bygroups(Comment.Preproc, Text, Keyword, Text, Comment.Preproc,
                      Comment, Comment.Preproc, Text, Keyword, Text,
                      Comment.Preproc)),
            # raw jinja blocks
            (r'(\{%)(-?\s*)(raw)(\s*-?)(%\})(.*?)'
             r'(\{%)(-?\s*)(endraw)(\s*-?)(%\})',
             bygroups(Comment.Preproc, Text, Keyword, Text, Comment.Preproc,
                      Text, Comment.Preproc, Text, Keyword, Text,
                      Comment.Preproc)),
            # filter blocks
            (r'(\{%)(-?\s*)(filter)(\s+)([a-zA-Z_]\w*)',
             bygroups(Comment.Preproc, Text, Keyword, Text, Name.Function),
             'block'),
            (r'(\{%)(-?\s*)([a-zA-Z_]\w*)',
             bygroups(Comment.Preproc, Text, Keyword), 'block'),
            (r'\{', Other)
        ],
        'varnames': [
            (r'(\|)(\s*)([a-zA-Z_]\w*)',
             bygroups(Operator, Text, Name.Function)),
            (r'(is)(\s+)(not)?(\s+)?([a-zA-Z_]\w*)',
             bygroups(Keyword, Text, Keyword, Text, Name.Function)),
            (r'(_|true|false|none|True|False|None)\b', Keyword.Pseudo),
            (r'(in|as|reversed|recursive|not|and|or|is|if|else|import|'
             r'with(?:(?:out)?\s*context)?|scoped|ignore\s+missing)\b',
             Keyword),
            (r'(loop|block|super|forloop)\b', Name.Builtin),
            (r'[a-zA-Z][\w-]*', Name.Variable),
            (r'\.\w+', Name.Variable),
            (r':?"(\\\\|\\"|[^"])*"', String.Double),
            (r":?'(\\\\|\\'|[^'])*'", String.Single),
            (r'([{}()\[\]+\-*/,:~]|[><=]=?)', Operator),
            (r"[0-9](\.[0-9]*)?(eE[+-][0-9])?[flFLdD]?|"
             r"0[xX][0-9a-fA-F]+[Ll]?", Number),
        ],
        'var': [
            (r'\s+', Text),
            (r'(-?)(\}\})', bygroups(Text, Comment.Preproc), '#pop'),
            include('varnames')
        ],
        'block': [
            (r'\s+', Text),
            (r'(-?)(%\})', bygroups(Text, Comment.Preproc), '#pop'),
            include('varnames'),
            (r'.', Punctuation)
        ]
    }

    def analyse_text(text):
        rv = 0.0
        if re.search(r'\{%\s*(block|extends)', text) is not None:
            rv += 0.4
        if re.search(r'\{%\s*if\s*.*?%\}', text) is not None:
            rv += 0.1
        if re.search(r'\{\{.*?\}\}', text) is not None:
            rv += 0.1
        return rv


class MyghtyLexer(RegexLexer):
    """
    Generic `myghty templates`_ lexer. Code that isn't Myghty
    markup is yielded as `Token.Other`.

    .. versionadded:: 0.6

    .. _myghty templates: http://www.myghty.org/
    """

    name = 'Myghty'
    aliases = ['myghty']
    filenames = ['*.myt', 'autodelegate']
    mimetypes = ['application/x-myghty']

    tokens = {
        'root': [
            (r'\s+', Text),
            (r'(<%(?:def|method))(\s*)(.*?)(>)(.*?)(</%\2\s*>)(?s)',
             bygroups(Name.Tag, Text, Name.Function, Name.Tag,
                      using(this), Name.Tag)),
            (r'(<%\w+)(.*?)(>)(.*?)(</%\2\s*>)(?s)',
             bygroups(Name.Tag, Name.Function, Name.Tag,
                      using(PythonLexer), Name.Tag)),
            (r'(<&[^|])(.*?)(,.*?)?(&>)',
             bygroups(Name.Tag, Name.Function, using(PythonLexer), Name.Tag)),
            (r'(<&\|)(.*?)(,.*?)?(&>)(?s)',
             bygroups(Name.Tag, Name.Function, using(PythonLexer), Name.Tag)),
            (r'</&>', Name.Tag),
            (r'(<%!?)(.*?)(%>)(?s)',
             bygroups(Name.Tag, using(PythonLexer), Name.Tag)),
            (r'(?<=^)#[^\n]*(\n|\Z)', Comment),
            (r'(?<=^)(%)([^\n]*)(\n|\Z)',
             bygroups(Name.Tag, using(PythonLexer), Other)),
            (r"""(?sx)
                 (.+?)               # anything, followed by:
                 (?:
                  (?<=\n)(?=[%#]) |  # an eval or comment line
                  (?=</?[%&]) |      # a substitution or block or
                                     # call start or end
                                     # - don't consume
                  (\\\n) |           # an escaped newline
                  \Z                 # end of string
                 )""", bygroups(Other, Operator)),
        ]
    }


class MyghtyXmlLexer(DelegatingLexer):
    """
    Subclass of the `MyghtyLexer` that highlights unlexed data
    with the `XmlLexer`.

    .. versionadded:: 0.6
    """

    name = 'XML+Myghty'
    aliases = ['xml+myghty']
    mimetypes = ['application/xml+myghty']

    def __init__(self, **options):
        super(MyghtyXmlLexer, self).__init__(XmlLexer, MyghtyLexer,
                                             **options)


class MyghtyCssLexer(DelegatingLexer):
    """
    Subclass of the `MyghtyLexer` that highlights unlexed data
    with the `CssLexer`.

    .. versionadded:: 0.6
    """

    name = 'CSS+Myghty'
    aliases = ['css+myghty']
    mimetypes = ['text/css+myghty']

    def __init__(self, **options):
        super(MyghtyCssLexer, self).__init__(CssLexer, MyghtyLexer,
                                             **options)


class MakoLexer(RegexLexer):
    """
    Generic `mako templates`_ lexer. Code that isn't Mako
    markup is yielded as `Token.Other`.

    .. versionadded:: 0.7

    .. _mako templates: http://www.makotemplates.org/
    """

    name = 'Mako'
    aliases = ['mako']
    filenames = ['*.mao']
    mimetypes = ['application/x-mako']

    tokens = {
        'root': [
            (r'(\s*)(%)(\s*end(?:\w+))(\n|\Z)',
             bygroups(Text, Comment.Preproc, Keyword, Other)),
            (r'(\s*)(%)([^\n]*)(\n|\Z)',
             bygroups(Text, Comment.Preproc, using(PythonLexer), Other)),
            (r'(\s*)(##[^\n]*)(\n|\Z)',
             bygroups(Text, Comment.Preproc, Other)),
            (r'(?s)<%doc>.*?</%doc>', Comment.Preproc),
            (r'(<%)([\w.:]+)',
             bygroups(Comment.Preproc, Name.Builtin), 'tag'),
            (r'(</%)([\w.:]+)(>)',
             bygroups(Comment.Preproc, Name.Builtin, Comment.Preproc)),
            (r'<%(?=([\w.:]+))', Comment.Preproc, 'ondeftags'),
            (r'(<%(?:!?))(.*?)(%>)(?s)',
             bygroups(Comment.Preproc, using(PythonLexer), Comment.Preproc)),
            (r'(\$\{)(.*?)(\})',
             bygroups(Comment.Preproc, using(PythonLexer), Comment.Preproc)),
            (r'''(?sx)
                (.+?)                # anything, followed by:
                (?:
                 (?<=\n)(?=%|\#\#) | # an eval or comment line
                 (?=\#\*) |          # multiline comment
                 (?=</?%) |          # a python block
                                     # call start or end
                 (?=\$\{) |          # a substitution
                 (?<=\n)(?=\s*%) |
                                     # - don't consume
                 (\\\n) |            # an escaped newline
                 \Z                  # end of string
                )
            ''', bygroups(Other, Operator)),
            (r'\s+', Text),
        ],
        'ondeftags': [
            (r'<%', Comment.Preproc),
            (r'(?<=<%)(include|inherit|namespace|page)', Name.Builtin),
            include('tag'),
        ],
        'tag': [
            (r'((?:\w+)\s*=)(\s*)(".*?")',
             bygroups(Name.Attribute, Text, String)),
            (r'/?\s*>', Comment.Preproc, '#pop'),
            (r'\s+', Text),
        ],
        'attr': [
            ('".*?"', String, '#pop'),
            ("'.*?'", String, '#pop'),
            (r'[^\s>]+', String, '#pop'),
        ],
    }


class MakoHtmlLexer(DelegatingLexer):
    """
    Subclass of the `MakoLexer` that highlights unlexed data
    with the `HtmlLexer`.

    .. versionadded:: 0.7
    """

    name = 'HTML+Mako'
    aliases = ['html+mako']
    mimetypes = ['text/html+mako']

    def __init__(self, **options):
        super(MakoHtmlLexer, self).__init__(MakoLexer,
                                            **options)


class MakoXmlLexer(DelegatingLexer):
    """
    Subclass of the `MakoLexer` that highlights unlexed data
    with the `XmlLexer`.

    .. versionadded:: 0.7
    """

    name = 'XML+Mako'
    aliases = ['xml+mako']
    mimetypes = ['application/xml+mako']

    def __init__(self, **options):
        super(MakoXmlLexer, self).__init__(XmlLexer, MakoLexer,
                                           **options)


class MakoJavascriptLexer(DelegatingLexer):
    """
    Subclass of the `MakoLexer` that highlights unlexed data
    with the `JavascriptLexer`.

    .. versionadded:: 0.7
    """

    name = 'JavaScript+Mako'
    aliases = ['js+mako', 'javascript+mako']
    mimetypes = ['application/x-javascript+mako',
                 'text/x-javascript+mako',
                 'text/javascript+mako']

    def __init__(self, **options):
        super(MakoJavascriptLexer, self).__init__(JavascriptLexer,
                                                  MakoLexer, **options)


class MakoCssLexer(DelegatingLexer):
    """
    Subclass of the `MakoLexer` that highlights unlexed data
    with the `CssLexer`.

    .. versionadded:: 0.7
    """

    name = 'CSS+Mako'
    aliases = ['css+mako']
    mimetypes = ['text/css+mako']

    def __init__(self, **options):
        super(MakoCssLexer, self).__init__(CssLexer, MakoLexer,
                                           **options)


# Genshi and Cheetah lexers courtesy of Matt Good.

class CheetahPythonLexer(Lexer):
    """
    Lexer for handling Cheetah's special $ tokens in Python syntax.
    """

    def get_tokens_unprocessed(self, text):
        pylexer = PythonLexer(**self.options)
        for pos, type_, value in pylexer.get_tokens_unprocessed(text):
            if type_ == Token.Error and value == '$':
                type_ = Comment.Preproc
            yield pos, type_, value


class CheetahLexer(RegexLexer):
    """
    Generic `cheetah templates`_ lexer. Code that isn't Cheetah
    markup is yielded as `Token.Other`.  This also works for
    `spitfire templates`_ which use the same syntax.

    .. _cheetah templates: http://www.cheetahtemplate.org/
    .. _spitfire templates: http://code.google.com/p/spitfire/
    """

    name = 'Cheetah'
    aliases = ['cheetah', 'spitfire']
    filenames = ['*.tmpl', '*.spt']
    mimetypes = ['application/x-cheetah', 'application/x-spitfire']

    tokens = {
        'root': [
            (r'(##[^\n]*)$',
             (bygroups(Comment))),
            (r'#[*](.|\n)*?[*]#', Comment),
            (r'#end[^#\n]*(?:#|$)', Comment.Preproc),
            (r'#slurp$', Comment.Preproc),
            (r'(#[a-zA-Z]+)([^#\n]*)(#|$)',
             (bygroups(Comment.Preproc, using(CheetahPythonLexer),
                       Comment.Preproc))),
            # TODO support other Python syntax like $foo['bar']
            (r'(\$)([a-zA-Z_][\w.]*\w)',
             bygroups(Comment.Preproc, using(CheetahPythonLexer))),
            (r'(\$\{!?)(.*?)(\})(?s)',
             bygroups(Comment.Preproc, using(CheetahPythonLexer),
                      Comment.Preproc)),
            (r'''(?sx)
                (.+?)               # anything, followed by:
                (?:
                 (?=\#[#a-zA-Z]*) | # an eval comment
                 (?=\$[a-zA-Z_{]) | # a substitution
                 \Z                 # end of string
                )
            ''', Other),
            (r'\s+', Text),
        ],
    }


class GenshiTextLexer(RegexLexer):
    """
    A lexer that highlights `genshi <http://genshi.edgewall.org/>`_ text
    templates.
    """

    name = 'Genshi Text'
    aliases = ['genshitext']
    mimetypes = ['application/x-genshi-text', 'text/x-genshi']

    tokens = {
        'root': [
            (r'[^#$\s]+', Other),
            (r'^(\s*)(##.*)$', bygroups(Text, Comment)),
            (r'^(\s*)(#)', bygroups(Text, Comment.Preproc), 'directive'),
            include('variable'),
            (r'[#$\s]', Other),
        ],
        'directive': [
            (r'\n', Text, '#pop'),
            (r'(?:def|for|if)\s+.*', using(PythonLexer), '#pop'),
            (r'(choose|when|with)([^\S\n]+)(.*)',
             bygroups(Keyword, Text, using(PythonLexer)), '#pop'),
            (r'(choose|otherwise)\b', Keyword, '#pop'),
            (r'(end\w*)([^\S\n]*)(.*)', bygroups(Keyword, Text, Comment), '#pop'),
        ],
        'variable': [
            (r'(?<!\$)(\$\{)(.+?)(\})',
             bygroups(Comment.Preproc, using(PythonLexer), Comment.Preproc)),
            (r'(?<!\$)(\$)([a-zA-Z_][\w.]*)',
             Name.Variable),
        ]
    }


class GenshiMarkupLexer(RegexLexer):
    """
    Base lexer for Genshi markup, used by `HtmlGenshiLexer` and
    `GenshiLexer`.
    """

    flags = re.DOTALL

    tokens = {
        'root': [
            (r'[^<$]+', Other),
            (r'(<\?python)(.*?)(\?>)',
             bygroups(Comment.Preproc, using(PythonLexer), Comment.Preproc)),
            # yield style and script blocks as Other
            (r'<\s*(script|style)\s*.*?>.*?<\s*/\1\s*>', Other),
            (r'<\s*py:[a-zA-Z0-9]+', Name.Tag, 'pytag'),
            (r'<\s*[a-zA-Z0-9:]+', Name.Tag, 'tag'),
            include('variable'),
            (r'[<$]', Other),
        ],
        'pytag': [
            (r'\s+', Text),
            (r'[\w:-]+\s*=', Name.Attribute, 'pyattr'),
            (r'/?\s*>', Name.Tag, '#pop'),
        ],
        'pyattr': [
            ('(")(.*?)(")', bygroups(String, using(PythonLexer), String), '#pop'),
            ("(')(.*?)(')", bygroups(String, using(PythonLexer), String), '#pop'),
            (r'[^\s>]+', String, '#pop'),
        ],
        'tag': [
            (r'\s+', Text),
            (r'py:[\w-]+\s*=', Name.Attribute, 'pyattr'),
            (r'[\w:-]+\s*=', Name.Attribute, 'attr'),
            (r'/?\s*>', Name.Tag, '#pop'),
        ],
        'attr': [
            ('"', String, 'attr-dstring'),
            ("'", String, 'attr-sstring'),
            (r'[^\s>]*', String, '#pop')
        ],
        'attr-dstring': [
            ('"', String, '#pop'),
            include('strings'),
            ("'", String)
        ],
        'attr-sstring': [
            ("'", String, '#pop'),
            include('strings'),
            ("'", String)
        ],
        'strings': [
            ('[^"\'$]+', String),
            include('variable')
        ],
        'variable': [
            (r'(?<!\$)(\$\{)(.+?)(\})',
             bygroups(Comment.Preproc, using(PythonLexer), Comment.Preproc)),
            (r'(?<!\$)(\$)([a-zA-Z_][\w\.]*)',
             Name.Variable),
        ]
    }


# class HtmlGenshiLexer(DelegatingLexer):
#     """
#     A lexer that highlights `genshi <http://genshi.edgewall.org/>`_ and
#     `kid <http://kid-templating.org/>`_ kid HTML templates.
#     """

#     name = 'HTML+Genshi'
#     aliases = ['html+genshi', 'html+kid']
#     alias_filenames = ['*.html', '*.htm', '*.xhtml']
#     mimetypes = ['text/html+genshi']

#     def __init__(self, **options):
#         super(HtmlGenshiLexer, self).__init__(GenshiMarkupLexer,
#                                               **options)

#     def analyse_text(text):
#         rv = 0.0
#         if re.search('\$\{.*?\}', text) is not None:
#             rv += 0.2
#         if re.search('py:(.*?)=["\']', text) is not None:
#             rv += 0.2
#         return rv + HtmlLexer.analyse_text(text) - 0.01


class GenshiLexer(DelegatingLexer):
    """
    A lexer that highlights `genshi <http://genshi.edgewall.org/>`_ and
    `kid <http://kid-templating.org/>`_ kid XML templates.
    """

    name = 'Genshi'
    aliases = ['genshi', 'kid', 'xml+genshi', 'xml+kid']
    filenames = ['*.kid']
    alias_filenames = ['*.xml']
    mimetypes = ['application/x-genshi', 'application/x-kid']

    def __init__(self, **options):
        super(GenshiLexer, self).__init__(XmlLexer, GenshiMarkupLexer,
                                          **options)

    def analyse_text(text):
        rv = 0.0
        if re.search(r'\$\{.*?\}', text) is not None:
            rv += 0.2
        if re.search('py:(.*?)=["\']', text) is not None:
            rv += 0.2
        return rv + XmlLexer.analyse_text(text) - 0.01


class JavascriptGenshiLexer(DelegatingLexer):
    """
    A lexer that highlights javascript code in genshi text templates.
    """

    name = 'JavaScript+Genshi Text'
    aliases = ['js+genshitext', 'js+genshi', 'javascript+genshitext',
               'javascript+genshi']
    alias_filenames = ['*.js']
    mimetypes = ['application/x-javascript+genshi',
                 'text/x-javascript+genshi',
                 'text/javascript+genshi']

    def __init__(self, **options):
        super(JavascriptGenshiLexer, self).__init__(JavascriptLexer,
                                                    GenshiTextLexer,
                                                    **options)

    def analyse_text(text):
        return GenshiLexer.analyse_text(text) - 0.05


class CssGenshiLexer(DelegatingLexer):
    """
    A lexer that highlights CSS definitions in genshi text templates.
    """

    name = 'CSS+Genshi Text'
    aliases = ['css+genshitext', 'css+genshi']
    alias_filenames = ['*.css']
    mimetypes = ['text/css+genshi']

    def __init__(self, **options):
        super(CssGenshiLexer, self).__init__(CssLexer, GenshiTextLexer,
                                             **options)

    def analyse_text(text):
        return GenshiLexer.analyse_text(text) - 0.05


class XmlErbLexer(DelegatingLexer):
    """
    Subclass of `ErbLexer` which highlights data outside preprocessor
    directives with the `XmlLexer`.
    """

    name = 'XML+Ruby'
    aliases = ['xml+erb', 'xml+ruby']
    alias_filenames = ['*.xml']
    mimetypes = ['application/xml+ruby']

    def __init__(self, **options):
        super(XmlErbLexer, self).__init__(XmlLexer, ErbLexer, **options)

    def analyse_text(text):
        rv = ErbLexer.analyse_text(text) - 0.01
        if looks_like_xml(text):
            rv += 0.4
        return rv


class CssErbLexer(DelegatingLexer):
    """
    Subclass of `ErbLexer` which highlights unlexed data with the `CssLexer`.
    """

    name = 'CSS+Ruby'
    aliases = ['css+erb', 'css+ruby']
    alias_filenames = ['*.css']
    mimetypes = ['text/css+ruby']

    def __init__(self, **options):
        super(CssErbLexer, self).__init__(CssLexer, ErbLexer, **options)

    def analyse_text(text):
        return ErbLexer.analyse_text(text) - 0.05


class XmlPhpLexer(DelegatingLexer):
    """
    Subclass of `PhpLexer` that higlights unhandled data with the `XmlLexer`.
    """

    name = 'XML+PHP'
    aliases = ['xml+php']
    alias_filenames = ['*.xml', '*.php', '*.php[345]']
    mimetypes = ['application/xml+php']

    def __init__(self, **options):
        super(XmlPhpLexer, self).__init__(XmlLexer, PhpLexer, **options)

    def analyse_text(text):
        rv = PhpLexer.analyse_text(text) - 0.01
        if looks_like_xml(text):
            rv += 0.4
        return rv


class CssPhpLexer(DelegatingLexer):
    """
    Subclass of `PhpLexer` which highlights unmatched data with the `CssLexer`.
    """

    name = 'CSS+PHP'
    aliases = ['css+php']
    alias_filenames = ['*.css']
    mimetypes = ['text/css+php']

    def __init__(self, **options):
        super(CssPhpLexer, self).__init__(CssLexer, PhpLexer, **options)

    def analyse_text(text):
        return PhpLexer.analyse_text(text) - 0.05


class JavascriptPhpLexer(DelegatingLexer):
    """
    Subclass of `PhpLexer` which highlights unmatched data with the
    `JavascriptLexer`.
    """

    name = 'JavaScript+PHP'
    aliases = ['js+php', 'javascript+php']
    alias_filenames = ['*.js']
    mimetypes = ['application/x-javascript+php',
                 'text/x-javascript+php',
                 'text/javascript+php']

    def __init__(self, **options):
        super(JavascriptPhpLexer, self).__init__(JavascriptLexer, PhpLexer,
                                                 **options)

    def analyse_text(text):
        return PhpLexer.analyse_text(text)


class XmlSmartyLexer(DelegatingLexer):
    """
    Subclass of the `SmartyLexer` that highlights unlexed data with the
    `XmlLexer`.
    """

    name = 'XML+Smarty'
    aliases = ['xml+smarty']
    alias_filenames = ['*.xml', '*.tpl']
    mimetypes = ['application/xml+smarty']

    def __init__(self, **options):
        super(XmlSmartyLexer, self).__init__(XmlLexer, SmartyLexer, **options)

    def analyse_text(text):
        rv = SmartyLexer.analyse_text(text) - 0.01
        if looks_like_xml(text):
            rv += 0.4
        return rv


class CssSmartyLexer(DelegatingLexer):
    """
    Subclass of the `SmartyLexer` that highlights unlexed data with the
    `CssLexer`.
    """

    name = 'CSS+Smarty'
    aliases = ['css+smarty']
    alias_filenames = ['*.css', '*.tpl']
    mimetypes = ['text/css+smarty']

    def __init__(self, **options):
        super(CssSmartyLexer, self).__init__(CssLexer, SmartyLexer, **options)

    def analyse_text(text):
        return SmartyLexer.analyse_text(text) - 0.05


class JavascriptSmartyLexer(DelegatingLexer):
    """
    Subclass of the `SmartyLexer` that highlights unlexed data with the
    `JavascriptLexer`.
    """

    name = 'JavaScript+Smarty'
    aliases = ['js+smarty', 'javascript+smarty']
    alias_filenames = ['*.js', '*.tpl']
    mimetypes = ['application/x-javascript+smarty',
                 'text/x-javascript+smarty',
                 'text/javascript+smarty']

    def __init__(self, **options):
        super(JavascriptSmartyLexer, self).__init__(JavascriptLexer, SmartyLexer,
                                                    **options)

    def analyse_text(text):
        return SmartyLexer.analyse_text(text) - 0.05


class XmlDjangoLexer(DelegatingLexer):
    """
    Subclass of the `DjangoLexer` that highlights unlexed data with the
    `XmlLexer`.
    """

    name = 'XML+Django/Jinja'
    aliases = ['xml+django', 'xml+jinja']
    alias_filenames = ['*.xml']
    mimetypes = ['application/xml+django', 'application/xml+jinja']

    def __init__(self, **options):
        super(XmlDjangoLexer, self).__init__(XmlLexer, DjangoLexer, **options)

    def analyse_text(text):
        rv = DjangoLexer.analyse_text(text) - 0.01
        if looks_like_xml(text):
            rv += 0.4
        return rv


class CssDjangoLexer(DelegatingLexer):
    """
    Subclass of the `DjangoLexer` that highlights unlexed data with the
    `CssLexer`.
    """

    name = 'CSS+Django/Jinja'
    aliases = ['css+django', 'css+jinja']
    alias_filenames = ['*.css']
    mimetypes = ['text/css+django', 'text/css+jinja']

    def __init__(self, **options):
        super(CssDjangoLexer, self).__init__(CssLexer, DjangoLexer, **options)

    def analyse_text(text):
        return DjangoLexer.analyse_text(text) - 0.05


class JavascriptDjangoLexer(DelegatingLexer):
    """
    Subclass of the `DjangoLexer` that highlights unlexed data with the
    `JavascriptLexer`.
    """

    name = 'JavaScript+Django/Jinja'
    aliases = ['js+django', 'javascript+django',
               'js+jinja', 'javascript+jinja']
    alias_filenames = ['*.js']
    mimetypes = ['application/x-javascript+django',
                 'application/x-javascript+jinja',
                 'text/x-javascript+django',
                 'text/x-javascript+jinja',
                 'text/javascript+django',
                 'text/javascript+jinja']

    def __init__(self, **options):
        super(JavascriptDjangoLexer, self).__init__(JavascriptLexer, DjangoLexer,
                                                    **options)

    def analyse_text(text):
        return DjangoLexer.analyse_text(text) - 0.05


class EvoqueLexer(RegexLexer):
    """
    For files using the Evoque templating system.

    .. versionadded:: 1.1
    """
    name = 'Evoque'
    aliases = ['evoque']
    filenames = ['*.evoque']
    mimetypes = ['application/x-evoque']

    flags = re.DOTALL

    tokens = {
        'root': [
            (r'[^#$]+', Other),
            (r'#\[', Comment.Multiline, 'comment'),
            (r'\$\$', Other),
            # svn keywords
            (r'\$\w+:[^$\n]*\$', Comment.Multiline),
            # directives: begin, end
            (r'(\$)(begin|end)(\{(%)?)(.*?)((?(4)%)\})',
             bygroups(Punctuation, Name.Builtin, Punctuation, None,
                      String, Punctuation)),
            # directives: evoque, overlay
            # see doc for handling first name arg: /directives/evoque/
            # + minor inconsistency: the "name" in e.g. $overlay{name=site_base}
            # should be using(PythonLexer), not passed out as String
            (r'(\$)(evoque|overlay)(\{(%)?)(\s*[#\w\-"\'.]+[^=,%}]+?)?'
             r'(.*?)((?(4)%)\})',
             bygroups(Punctuation, Name.Builtin, Punctuation, None,
                      String, using(PythonLexer), Punctuation)),
            # directives: if, for, prefer, test
            (r'(\$)(\w+)(\{(%)?)(.*?)((?(4)%)\})',
             bygroups(Punctuation, Name.Builtin, Punctuation, None,
                      using(PythonLexer), Punctuation)),
            # directive clauses (no {} expression)
            (r'(\$)(else|rof|fi)', bygroups(Punctuation, Name.Builtin)),
            # expressions
            (r'(\$\{(%)?)(.*?)((!)(.*?))?((?(2)%)\})',
             bygroups(Punctuation, None, using(PythonLexer),
                      Name.Builtin, None, None, Punctuation)),
            (r'#', Other),
        ],
        'comment': [
            (r'[^\]#]', Comment.Multiline),
            (r'#\[', Comment.Multiline, '#push'),
            (r'\]#', Comment.Multiline, '#pop'),
            (r'[\]#]', Comment.Multiline)
        ],
    }


class EvoqueXmlLexer(DelegatingLexer):
    """
    Subclass of the `EvoqueLexer` that highlights unlexed data with the
    `XmlLexer`.

    .. versionadded:: 1.1
    """
    name = 'XML+Evoque'
    aliases = ['xml+evoque']
    filenames = ['*.xml']
    mimetypes = ['application/xml+evoque']

    def __init__(self, **options):
        super(EvoqueXmlLexer, self).__init__(XmlLexer, EvoqueLexer,
                                             **options)


class ColdfusionLexer(RegexLexer):
    """
    Coldfusion statements
    """
    name = 'cfstatement'
    aliases = ['cfs']
    filenames = []
    mimetypes = []
    flags = re.IGNORECASE

    tokens = {
        'root': [
            (r'//.*?\n', Comment.Single),
            (r'/\*(?:.|\n)*?\*/', Comment.Multiline),
            (r'\+\+|--', Operator),
            (r'[-+*/^&=!]', Operator),
            (r'<=|>=|<|>|==', Operator),
            (r'mod\b', Operator),
            (r'(eq|lt|gt|lte|gte|not|is|and|or)\b', Operator),
            (r'\|\||&&', Operator),
            (r'\?', Operator),
            (r'"', String.Double, 'string'),
            # There is a special rule for allowing html in single quoted
            # strings, evidently.
            (r"'.*?'", String.Single),
            (r'\d+', Number),
            (r'(if|else|len|var|xml|default|break|switch|component|property|function|do|'
             r'try|catch|in|continue|for|return|while|required|any|array|binary|boolean|'
             r'component|date|guid|numeric|query|string|struct|uuid|case)\b', Keyword),
            (r'(true|false|null)\b', Keyword.Constant),
            (r'(application|session|client|cookie|super|this|variables|arguments)\b',
             Name.Constant),
            (r'([a-z_$][\w.]*)(\s*)(\()',
             bygroups(Name.Function, Text, Punctuation)),
            (r'[a-z_$][\w.]*', Name.Variable),
            (r'[()\[\]{};:,.\\]', Punctuation),
            (r'\s+', Text),
        ],
        'string': [
            (r'""', String.Double),
            (r'#.+?#', String.Interp),
            (r'[^"#]+', String.Double),
            (r'#', String.Double),
            (r'"', String.Double, '#pop'),
        ],
    }


class ColdfusionMarkupLexer(RegexLexer):
    """
    Coldfusion markup only
    """
    name = 'Coldfusion'
    aliases = ['cf']
    filenames = []
    mimetypes = []

    tokens = {
        'root': [
            (r'[^<]+', Other),
            include('tags'),
            (r'<[^<>]*', Other),
        ],
        'tags': [
            (r'<!---', Comment.Multiline, 'cfcomment'),
            (r'(?s)<!--.*?-->', Comment),
            (r'<cfoutput.*?>', Name.Builtin, 'cfoutput'),
            (r'(?s)(<cfscript.*?>)(.+?)(</cfscript.*?>)',
             bygroups(Name.Builtin, using(ColdfusionLexer), Name.Builtin)),
            # negative lookbehind is for strings with embedded >
            (r'(?s)(</?cf(?:component|include|if|else|elseif|loop|return|'
             r'dbinfo|dump|abort|location|invoke|throw|file|savecontent|'
             r'mailpart|mail|header|content|zip|image|lock|argument|try|'
             r'catch|break|directory|http|set|function|param)\b)(.*?)((?<!\\)>)',
             bygroups(Name.Builtin, using(ColdfusionLexer), Name.Builtin)),
        ],
        'cfoutput': [
            (r'[^#<]+', Other),
            (r'(#)(.*?)(#)', bygroups(Punctuation, using(ColdfusionLexer),
                                      Punctuation)),
            # (r'<cfoutput.*?>', Name.Builtin, '#push'),
            (r'</cfoutput.*?>', Name.Builtin, '#pop'),
            include('tags'),
            (r'(?s)<[^<>]*', Other),
            (r'#', Other),
        ],
        'cfcomment': [
            (r'<!---', Comment.Multiline, '#push'),
            (r'--->', Comment.Multiline, '#pop'),
            (r'([^<-]|<(?!!---)|-(?!-->))+', Comment.Multiline),
        ],
    }


class ColdfusionHtmlLexer(DelegatingLexer):
    """
    Coldfusion markup in html
    """
    name = 'Coldfusion HTML'
    aliases = ['cfm']
    filenames = ['*.cfm', '*.cfml']
    mimetypes = ['application/x-coldfusion']

    def __init__(self, **options):
        super(ColdfusionHtmlLexer, self).__init__(ColdfusionMarkupLexer,
                                                  **options)


class ColdfusionCFCLexer(DelegatingLexer):
    """
    Coldfusion markup/script components

    .. versionadded:: 2.0
    """
    name = 'Coldfusion CFC'
    aliases = ['cfc']
    filenames = ['*.cfc']
    mimetypes = []

    def __init__(self, **options):
        super(ColdfusionCFCLexer, self).__init__(ColdfusionHtmlLexer, ColdfusionLexer,
                                                 **options)


class LassoHtmlLexer(DelegatingLexer):
    """
    Subclass of the `LassoLexer` which highlights unhandled data with the
    `HtmlLexer`.

    Nested JavaScript and CSS is also highlighted.

    .. versionadded:: 1.6
    """

    name = 'HTML+Lasso'
    aliases = ['html+lasso']
    alias_filenames = ['*.html', '*.htm', '*.xhtml', '*.lasso', '*.lasso[89]',
                       '*.incl', '*.inc', '*.las']
    mimetypes = ['text/html+lasso',
                 'application/x-httpd-lasso',
                 'application/x-httpd-lasso[89]']

    def __init__(self, **options):
        super(LassoHtmlLexer, self).__init__(LassoLexer, **options)

    def analyse_text(text):
        rv = LassoLexer.analyse_text(text) - 0.01
        if html_doctype_matches(text):  # same as HTML lexer
            rv += 0.5
        return rv


class LassoXmlLexer(DelegatingLexer):
    """
    Subclass of the `LassoLexer` which highlights unhandled data with the
    `XmlLexer`.

    .. versionadded:: 1.6
    """

    name = 'XML+Lasso'
    aliases = ['xml+lasso']
    alias_filenames = ['*.xml', '*.lasso', '*.lasso[89]',
                       '*.incl', '*.inc', '*.las']
    mimetypes = ['application/xml+lasso']

    def __init__(self, **options):
        super(LassoXmlLexer, self).__init__(XmlLexer, LassoLexer, **options)

    def analyse_text(text):
        rv = LassoLexer.analyse_text(text) - 0.01
        if looks_like_xml(text):
            rv += 0.4
        return rv


class LassoCssLexer(DelegatingLexer):
    """
    Subclass of the `LassoLexer` which highlights unhandled data with the
    `CssLexer`.

    .. versionadded:: 1.6
    """

    name = 'CSS+Lasso'
    aliases = ['css+lasso']
    alias_filenames = ['*.css']
    mimetypes = ['text/css+lasso']

    def __init__(self, **options):
        options['requiredelimiters'] = True
        super(LassoCssLexer, self).__init__(CssLexer, LassoLexer, **options)

    def analyse_text(text):
        rv = LassoLexer.analyse_text(text) - 0.05
        if re.search(r'\w+:.+?;', text):
            rv += 0.1
        if 'padding:' in text:
            rv += 0.1
        return rv


class LassoJavascriptLexer(DelegatingLexer):
    """
    Subclass of the `LassoLexer` which highlights unhandled data with the
    `JavascriptLexer`.

    .. versionadded:: 1.6
    """

    name = 'JavaScript+Lasso'
    aliases = ['js+lasso', 'javascript+lasso']
    alias_filenames = ['*.js']
    mimetypes = ['application/x-javascript+lasso',
                 'text/x-javascript+lasso',
                 'text/javascript+lasso']

    def __init__(self, **options):
        options['requiredelimiters'] = True
        super(LassoJavascriptLexer, self).__init__(JavascriptLexer, LassoLexer,
                                                   **options)

    def analyse_text(text):
        rv = LassoLexer.analyse_text(text) - 0.05
        if 'function' in text:
            rv += 0.2
        return rv


class HandlebarsLexer(RegexLexer):
    """
    Generic `handlebars <http://handlebarsjs.com/>` template lexer.

    Highlights only the Handlebars template tags (stuff between `{{` and `}}`).
    Everything else is left for a delegating lexer.

    .. versionadded:: 2.0
    """

    name = "Handlebars"
    aliases = ['handlebars']

    tokens = {
        'root': [
            (r'[^{]+', Other),

            (r'\{\{!.*\}\}', Comment),

            (r'(\{\{\{)(\s*)', bygroups(Comment.Special, Text), 'tag'),
            (r'(\{\{)(\s*)', bygroups(Comment.Preproc, Text), 'tag'),
        ],

        'tag': [
            (r'\s+', Text),
            (r'\}\}\}', Comment.Special, '#pop'),
            (r'\}\}', Comment.Preproc, '#pop'),

            # Handlebars
            (r'([#/]*)(each|if|unless|else|with|log|in)', bygroups(Keyword,
             Keyword)),

            # General {{#block}}
            (r'([#/])([\w-]+)', bygroups(Name.Function, Name.Function)),

            # {{opt=something}}
            (r'([\w-]+)(=)', bygroups(Name.Attribute, Operator)),

            # borrowed from DjangoLexer
            (r':?"(\\\\|\\"|[^"])*"', String.Double),
            (r":?'(\\\\|\\'|[^'])*'", String.Single),
            (r'[a-zA-Z][\w-]*', Name.Variable),
            (r'\.[\w-]+', Name.Variable),
            (r"[0-9](\.[0-9]*)?(eE[+-][0-9])?[flFLdD]?|"
             r"0[xX][0-9a-fA-F]+[Ll]?", Number),
        ]
    }


class YamlJinjaLexer(DelegatingLexer):
    """
    Subclass of the `DjangoLexer` that highighlights unlexed data with the
    `YamlLexer`.

    Commonly used in Saltstack salt states.

    .. versionadded:: 2.0
    """

    name = 'YAML+Jinja'
    aliases = ['yaml+jinja', 'salt', 'sls']
    filenames = ['*.sls']
    mimetypes = ['text/x-yaml+jinja', 'text/x-sls']

    def __init__(self, **options):
        super(YamlJinjaLexer, self).__init__(YamlLexer, DjangoLexer, **options)


class LiquidLexer(RegexLexer):
    """
    Lexer for `Liquid templates
    <http://www.rubydoc.info/github/Shopify/liquid>`_.

    .. versionadded:: 2.0
    """
    name = 'liquid'
    aliases = ['liquid']
    filenames = ['*.liquid']

    tokens = {
        'root': [
            (r'[^{]+', Text),
            # tags and block tags
            (r'(\{%)(\s*)', bygroups(Punctuation, Whitespace), 'tag-or-block'),
            # output tags
            (r'(\{\{)(\s*)([^\s}]+)',
             bygroups(Punctuation, Whitespace, using(this, state = 'generic')),
             'output'),
            (r'\{', Text)
        ],

        'tag-or-block': [
            # builtin logic blocks
            (r'(if|unless|elsif|case)(?=\s+)', Keyword.Reserved, 'condition'),
            (r'(when)(\s+)', bygroups(Keyword.Reserved, Whitespace),
             combined('end-of-block', 'whitespace', 'generic')),
            (r'(else)(\s*)(%\})',
             bygroups(Keyword.Reserved, Whitespace, Punctuation), '#pop'),

            # other builtin blocks
            (r'(capture)(\s+)([^\s%]+)(\s*)(%\})',
             bygroups(Name.Tag, Whitespace, using(this, state = 'variable'),
                      Whitespace, Punctuation), '#pop'),
            (r'(comment)(\s*)(%\})',
             bygroups(Name.Tag, Whitespace, Punctuation), 'comment'),
            (r'(raw)(\s*)(%\})',
             bygroups(Name.Tag, Whitespace, Punctuation), 'raw'),

            # end of block
            (r'(end(case|unless|if))(\s*)(%\})',
             bygroups(Keyword.Reserved, None, Whitespace, Punctuation), '#pop'),
            (r'(end([^\s%]+))(\s*)(%\})',
             bygroups(Name.Tag, None, Whitespace, Punctuation), '#pop'),

            # builtin tags (assign and include are handled together with usual tags)
            (r'(cycle)(\s+)(?:([^\s:]*)(:))?(\s*)',
             bygroups(Name.Tag, Whitespace,
                      using(this, state='generic'), Punctuation, Whitespace),
             'variable-tag-markup'),

            # other tags or blocks
            (r'([^\s%]+)(\s*)', bygroups(Name.Tag, Whitespace), 'tag-markup')
        ],

        'output': [
            include('whitespace'),
            (r'\}\}', Punctuation, '#pop'),  # end of output

            (r'\|', Punctuation, 'filters')
        ],

        'filters': [
            include('whitespace'),
            (r'\}\}', Punctuation, ('#pop', '#pop')),  # end of filters and output

            (r'([^\s|:]+)(:?)(\s*)',
             bygroups(Name.Function, Punctuation, Whitespace), 'filter-markup')
        ],

        'filter-markup': [
            (r'\|', Punctuation, '#pop'),
            include('end-of-tag'),
            include('default-param-markup')
        ],

        'condition': [
            include('end-of-block'),
            include('whitespace'),

            (r'([^\s=!><]+)(\s*)([=!><]=?)(\s*)(\S+)(\s*)(%\})',
             bygroups(using(this, state = 'generic'), Whitespace, Operator,
                      Whitespace, using(this, state = 'generic'), Whitespace,
                      Punctuation)),
            (r'\b!', Operator),
            (r'\bnot\b', Operator.Word),
            (r'([\w.\'"]+)(\s+)(contains)(\s+)([\w.\'"]+)',
             bygroups(using(this, state = 'generic'), Whitespace, Operator.Word,
                      Whitespace, using(this, state = 'generic'))),

            include('generic'),
            include('whitespace')
        ],

        'generic-value': [
            include('generic'),
            include('end-at-whitespace')
        ],

        'operator': [
            (r'(\s*)((=|!|>|<)=?)(\s*)',
             bygroups(Whitespace, Operator, None, Whitespace), '#pop'),
            (r'(\s*)(\bcontains\b)(\s*)',
             bygroups(Whitespace, Operator.Word, Whitespace), '#pop'),
        ],

        'end-of-tag': [
            (r'\}\}', Punctuation, '#pop')
        ],

        'end-of-block': [
            (r'%\}', Punctuation, ('#pop', '#pop'))
        ],

        'end-at-whitespace': [
            (r'\s+', Whitespace, '#pop')
        ],

        # states for unknown markup
        'param-markup': [
            include('whitespace'),
            # params with colons or equals
            (r'([^\s=:]+)(\s*)(=|:)',
             bygroups(Name.Attribute, Whitespace, Operator)),
            # explicit variables
            (r'(\{\{)(\s*)([^\s}])(\s*)(\}\})',
             bygroups(Punctuation, Whitespace, using(this, state = 'variable'),
                      Whitespace, Punctuation)),

            include('string'),
            include('number'),
            include('keyword'),
            (r',', Punctuation)
        ],

        'default-param-markup': [
            include('param-markup'),
            (r'.', Text)  # fallback for switches / variables / un-quoted strings / ...
        ],

        'variable-param-markup': [
            include('param-markup'),
            include('variable'),
            (r'.', Text)  # fallback
        ],

        'tag-markup': [
            (r'%\}', Punctuation, ('#pop', '#pop')),  # end of tag
            include('default-param-markup')
        ],

        'variable-tag-markup': [
            (r'%\}', Punctuation, ('#pop', '#pop')),  # end of tag
            include('variable-param-markup')
        ],

        # states for different values types
        'keyword': [
            (r'\b(false|true)\b', Keyword.Constant)
        ],

        'variable': [
            (r'[a-zA-Z_]\w*', Name.Variable),
            (r'(?<=\w)\.(?=\w)', Punctuation)
        ],

        'string': [
            (r"'[^']*'", String.Single),
            (r'"[^"]*"', String.Double)
        ],

        'number': [
            (r'\d+\.\d+', Number.Float),
            (r'\d+', Number.Integer)
        ],

        'generic': [  # decides for variable, string, keyword or number
            include('keyword'),
            include('string'),
            include('number'),
            include('variable')
        ],

        'whitespace': [
            (r'[ \t]+', Whitespace)
        ],

        # states for builtin blocks
        'comment': [
            (r'(\{%)(\s*)(endcomment)(\s*)(%\})',
             bygroups(Punctuation, Whitespace, Name.Tag, Whitespace,
                      Punctuation), ('#pop', '#pop')),
            (r'.', Comment)
        ],

        'raw': [
            (r'[^{]+', Text),
            (r'(\{%)(\s*)(endraw)(\s*)(%\})',
             bygroups(Punctuation, Whitespace, Name.Tag, Whitespace,
                      Punctuation), '#pop'),
            (r'\{', Text)
        ],
    }


class TwigLexer(RegexLexer):
    """
    `Twig <http://twig.sensiolabs.org/>`_ template lexer.

    It just highlights Twig code between the preprocessor directives,
    other data is left untouched by the lexer.

    .. versionadded:: 2.0
    """

    name = 'Twig'
    aliases = ['twig']
    mimetypes = ['application/x-twig']

    flags = re.M | re.S

    # Note that a backslash is included in the following two patterns
    # PHP uses a backslash as a namespace separator
    _ident_char = r'[\\\w-]|[^\x00-\x7f]'
    _ident_begin = r'(?:[\\_a-z]|[^\x00-\x7f])'
    _ident_end = r'(?:' + _ident_char + ')*'
    _ident_inner = _ident_begin + _ident_end

    tokens = {
        'root': [
            (r'[^{]+', Other),
            (r'\{\{', Comment.Preproc, 'var'),
            # twig comments
            (r'\{\#.*?\#\}', Comment),
            # raw twig blocks
            (r'(\{%)(-?\s*)(raw)(\s*-?)(%\})(.*?)'
             r'(\{%)(-?\s*)(endraw)(\s*-?)(%\})',
             bygroups(Comment.Preproc, Text, Keyword, Text, Comment.Preproc,
                      Other, Comment.Preproc, Text, Keyword, Text,
                      Comment.Preproc)),
            (r'(\{%)(-?\s*)(verbatim)(\s*-?)(%\})(.*?)'
             r'(\{%)(-?\s*)(endverbatim)(\s*-?)(%\})',
             bygroups(Comment.Preproc, Text, Keyword, Text, Comment.Preproc,
                      Other, Comment.Preproc, Text, Keyword, Text,
                      Comment.Preproc)),
            # filter blocks
            (r'(\{%%)(-?\s*)(filter)(\s+)(%s)' % _ident_inner,
             bygroups(Comment.Preproc, Text, Keyword, Text, Name.Function),
             'tag'),
            (r'(\{%)(-?\s*)([a-zA-Z_]\w*)',
             bygroups(Comment.Preproc, Text, Keyword), 'tag'),
            (r'\{', Other),
        ],
        'varnames': [
            (r'(\|)(\s*)(%s)' % _ident_inner,
             bygroups(Operator, Text, Name.Function)),
            (r'(is)(\s+)(not)?(\s*)(%s)' % _ident_inner,
             bygroups(Keyword, Text, Keyword, Text, Name.Function)),
            (r'(?i)(true|false|none|null)\b', Keyword.Pseudo),
            (r'(in|not|and|b-and|or|b-or|b-xor|is'
             r'if|elseif|else|import'
             r'constant|defined|divisibleby|empty|even|iterable|odd|sameas'
             r'matches|starts\s+with|ends\s+with)\b',
             Keyword),
            (r'(loop|block|parent)\b', Name.Builtin),
            (_ident_inner, Name.Variable),
            (r'\.' + _ident_inner, Name.Variable),
            (r'\.[0-9]+', Number),
            (r':?"(\\\\|\\"|[^"])*"', String.Double),
            (r":?'(\\\\|\\'|[^'])*'", String.Single),
            (r'([{}()\[\]+\-*/,:~%]|\.\.|\?|:|\*\*|\/\/|!=|[><=]=?)', Operator),
            (r"[0-9](\.[0-9]*)?(eE[+-][0-9])?[flFLdD]?|"
             r"0[xX][0-9a-fA-F]+[Ll]?", Number),
        ],
        'var': [
            (r'\s+', Text),
            (r'(-?)(\}\})', bygroups(Text, Comment.Preproc), '#pop'),
            include('varnames')
        ],
        'tag': [
            (r'\s+', Text),
            (r'(-?)(%\})', bygroups(Text, Comment.Preproc), '#pop'),
            include('varnames'),
            (r'.', Punctuation),
        ],
    }


class TwigHtmlLexer(DelegatingLexer):
    """
    Subclass of the `TwigLexer` that highlights unlexed data with the
    `HtmlLexer`.

    .. versionadded:: 2.0
    """

    name = "HTML+Twig"
    aliases = ["html+twig"]
    filenames = ['*.twig']
    mimetypes = ['text/html+twig']

    def __init__(self, **options):
        super(TwigHtmlLexer, self).__init__(TwigLexer, **options)
