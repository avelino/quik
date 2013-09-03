#!/usr/bin/env python
from setuptools import setup


setup(name="quik",
      version="0.1",
      description="A fast and lightweight Python template engine",
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
