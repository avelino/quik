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

