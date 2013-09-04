#!/usr/bin/env python
# -*- coding: utf-8 -*-
from quik import CachingFileLoader

from jinja2 import Environment, FileSystemLoader, TemplateNotFound


data = {'author': 'Thiago Avelino'}


@profile
def quik(template_name):
    loader = CachingFileLoader('html')
    template = loader.load_template(template_name)
    return template.render(data, loader=loader).encode('utf-8')


@profile
def jinja2(template_name):
    env = Environment(loader=FileSystemLoader(['html']))
    try:
        template = env.get_template(template_name)
    except TemplateNotFound:
        raise TemplateNotFound(template_name)

    return template.render(data).encode('utf-8')


quik('quik.html')
quik('quik.html')
jinja2('jinja2.html')
jinja2('jinja2.html')
