quik
====

.. image:: https://travis-ci.org/avelino/quik.png?branch=master
    :target: https://travis-ci.org/avelino/quik
    :alt: Build Status - Travis CI

A fast and lightweight Python template engine


Nutshell
--------

Here a small example of a Quik template

.. code-block:: html

    <ul>
        #for ($user in $users)
            #if($user.age > 18)
            <li><a href="$user.url">$user.username</a></li>
            #end
        #end
    </ul>


Use It
------

Render via template:

.. code-block:: python

    from quik import CachingFileLoader

    loader = CachingFileLoader('html')
    template = loader.load_template('index.html')
    print template.merge({'author': 'Thiago Avelino'},
                         loader=loader).encode('utf-8')


Features
--------

- Easy to use.
- High performance.
- Autoescaping.
- Template inheritance.
- Supports native python expressions.
