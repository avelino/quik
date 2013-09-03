#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, operator, os
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
    xrange = range


class Template:
    def __init__(self, content):
        self.content = content
        self.root_element = None

    def merge(self, namespace, loader=None):
        output = StoppableStream()
        self.merge_to(namespace, output, loader)
        return output.getvalue()

    def ensure_compiled(self):
        if not self.root_element:
            self.root_element = TemplateBody(self.content)

    def merge_to(self, namespace, fileobj, loader=None):
        if loader is None: loader = NullLoader()
        self.ensure_compiled()
        self.root_element.evaluate(fileobj, namespace, loader)


class TemplateError(Exception):
    pass


class TemplateSyntaxError(TemplateError):
    def __init__(self, element, expected):
        self.element = element
        self.text_understood = element.full_text()[:element.end]
        self.line = 1 + self.text_understood.count('\n')
        self.column = len(self.text_understood) - self.text_understood.rfind('\n')
        got = element.next_text()
        if len(got) > 40:
            got = got[:36] + ' ...'
        Exception.__init__(self, "line %d, column %d: expected %s in %s, got: %s ..." % (self.line, self.column, expected, self.element_name(), got))

    def get_position_strings(self):
        error_line_start = 1 + self.text_understood.rfind('\n')
        if '\n' in self.element.next_text():
            error_line_end = self.element.next_text().find('\n') + self.element.end
        else:
            error_line_end = len(self.element.full_text())
        error_line = self.element.full_text()[error_line_start:error_line_end]
        caret_pos = self.column
        return [error_line, ' ' * (caret_pos - 1) + '^']

    def element_name(self):
        return re.sub('([A-Z])', lambda m: ' ' + m.group(1).lower(), self.element.__class__.__name__).strip()


class NullLoader:
    def load_text(self, name):
        raise TemplateError("no loader available for '%s'" % name)

    def load_template(self, name):
        raise self.load_text(name)


class CachingFileLoader:
    def __init__(self, basedir, debugging=False):
        self.basedir = basedir
        self.known_templates = {}
        self.debugging = debugging
        if debugging:
            print("creating caching file loader with basedir: {0}".format(basedir))

    def filename_of(self, name):
        return os.path.join(self.basedir, name)

    def load_text(self, name):
        if self.debugging:
            print("Loading text from {0} {1}".format(self.basedir, name))
        f = open(self.filename_of(name))
        try: return f.read()
        finally: f.close()

    def load_template(self, name):
        if self.debugging:
            print("Loading template... {0}".format(name))
        mtime = os.path.getmtime(self.filename_of(name))
        if self.known_templates.get(name, None):
            template, prev_mtime = self.known_templates[name]
            if mtime <= prev_mtime:
                if self.debugging:
                    print("loading parsed template from cache")
                return template
        if self.debugging:
            print("loading text from disk")
        template = Template(self.load_text(name))
        template.ensure_compiled()
        self.known_templates[name] = (template, mtime)
        return template


class StoppableStream(StringIO):
    def __init__(self, buf=''):
        self.stop = False
        StringIO.__init__(self, buf)

    def write(self, s):
        if not self.stop:
            StringIO.write(self, s)


WHITESPACE_TO_END_OF_LINE = re.compile(r'[ \t\r]*\n(.*)', re.S)

class NoMatch(Exception): pass


class LocalNamespace(dict):
    def __init__(self, parent):
        dict.__init__(self)
        self.parent = parent

    def __getitem__(self, key):
        try: return dict.__getitem__(self, key)
        except KeyError:
            parent_value = self.parent[key]
            self[key] = parent_value
            return parent_value

    def top(self):
        if hasattr(self.parent, "top"):
            return self.parent.top()
        return self.parent

    def __repr__(self):
        return dict.__repr__(self) + '->' + repr(self.parent)


class _Element:
    def __init__(self, text, start=0):
        self._full_text = text
        self.start = self.end = start
        self.parse()

    def next_text(self):
        return self._full_text[self.end:]

    def my_text(self):
        return self._full_text[self.start:self.end]

    def full_text(self):
        return self._full_text

    def syntax_error(self, expected):
        return TemplateSyntaxError(self, expected)

    def identity_match(self, pattern):
        m = pattern.match(self._full_text, self.end)
        if not m: raise NoMatch()
        self.end = m.start(pattern.groups)
        return m.groups()[:-1]

    def next_match(self, pattern):
        m = pattern.match(self._full_text, self.end)
        if not m: return False
        self.end = m.start(pattern.groups)
        return m.groups()[:-1]

    def optional_match(self, pattern):
        m = pattern.match(self._full_text, self.end)
        if not m: return False
        self.end = m.start(pattern.groups)
        return True

    def require_match(self, pattern, expected):
        m = pattern.match(self._full_text, self.end)
        if not m: raise self.syntax_error(expected)
        self.end = m.start(pattern.groups)
        return m.groups()[:-1]

    def next_element(self, element_spec):
        if callable(element_spec):
            element = element_spec(self._full_text, self.end)
            self.end = element.end
            return element
        else:
            for element_class in element_spec:
                try: element = element_class(self._full_text, self.end)
                except NoMatch: pass
                else:
                    self.end = element.end
                    return element
            raise NoMatch()

    def require_next_element(self, element_spec, expected):
        if callable(element_spec):
            try: element = element_spec(self._full_text, self.end)
            except NoMatch: raise self.syntax_error(expected)
            else:
                self.end = element.end
                return element
        else:
            for element_class in element_spec:
                try: element = element_class(self._full_text, self.end)
                except NoMatch: pass
                else:
                    self.end = element.end
                    return element
            expected = ', '.join([cls.__name__ for cls in element_spec])
            raise self.syntax_error('one of: ' + expected)
