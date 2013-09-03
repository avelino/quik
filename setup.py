#!/usr/bin/env python
from setuptools import setup


long_description = open('README.rst').read()

setup(name="quik",
      version="0.2.1",
      description="A fast and lightweight Python template engine",
      long_description=long_description,
      author="Thiago Avelino",
      author_email="thiago@avelino.xxx",
      url="https://github.com/avelino/quik",
      license="MIT",
      py_modules=['quik'],
      zip_safe=False,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Text Processing :: Markup :: HTML'],
      keywords="template, engine, web, fast, lightweight",
      include_package_data=True,)
