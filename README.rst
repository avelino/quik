====
Quik
====

.. image:: https://travis-ci.org/avelino/quik.png?branch=master
    :target: https://travis-ci.org/avelino/quik
    :alt: Build Status - Travis CI

A fast and lightweight Python template engine


Features
--------

- Easy to use.
- High performance.
- Autoescaping.
- Template inheritance.
- Supports native python expressions.


Install
-------

.. code-block:: shell

    pip install quik

or developer mode:

.. code-block:: shell

    pip install -r git+https://github.com/avelino/quik.git#egg=quik


Nutshell
--------

Here a small example of a Quik template

.. code-block:: html

    <ul>
        #for @user in @users:
            #if @user.age > 18:
            <li><a href="@user.url">@user.username</a></li>
            #end
        #end
    </ul>


Use It
------

Render via template:

.. code-block:: python

    from quik import FileLoader

    loader = FileLoader('html')
    template = loader.load_template('index.html')
    print template.render({'author': 'Thiago Avelino'},
                          loader=loader).encode('utf-8')


Render via string:

.. code-block:: python

    from quik import Template

    temp = Template("""
    <ul>
        #for @user in @users:
            #if @user.age > 18:
            <li><a href="@user.url">@user.username</a></li>
            #end
        #end
    </ul>
    """)

    users = [
        {'username': 'foo', 'url': 'http://...', 'age': 25},
        {'username': 'bar', 'url': 'https://...', 'age': 18}]

    print temp.render(locals())

