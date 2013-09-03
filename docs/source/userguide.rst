==========
User Guide
==========


About this Guide
================

The Quik User Guide is intended to help page designers and content providers get acquainted with Quik and the syntax of its simple yet powerful scripting language, the Quik Template Language (QTL). Many of the examples in this guide deal with using Quik to embed dynamic content in web sites, but all QTL examples are equally applicable to other pages and templates.

Thanks for choosing Quik!


Hello Quik World!
=================

Once a value has been assigned to a variable, you can reference the variable anywhere in your HTML document. In the following example, a value is assigned to $foo and later referenced.

.. code-block:: html

    <html>
        <body>
            #set( $foo = "Quik" )
            Hello $foo World!
        </body>
    <html>

The result is a web page that prints "Hello Quik World!".
To make statements containing QTL directives more readable, we encourage you to start each QTL statement on a new line, although you are not required to do so. The set directive will be revisited in greater detail later on.
