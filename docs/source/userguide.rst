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
            #set( @foo = "Quik" )
            Hello @foo World!
        </body>
    <html>

The result is a web page that prints "Hello Quik World!".
To make statements containing QTL directives more readable, we encourage you to start each QTL statement on a new line, although you are not required to do so. The set directive will be revisited in greater detail later on.


Comments
========

Comments allows descriptive text to be included that is not placed into the output of the template engine. Comments are a useful way of reminding yourself and explaining to others what your QTL statements are doing, or any other purpose you find useful. Below is an example of a comment in QTL.


.. code-block:: html

    ## This is a single line comment.

A single line comment begins with ## and finishes at the end of the line. If you're going to write a few lines of commentary, there's no need to have numerous single line comments. Multi-line comments, which begin with #* and end with \*#, are available to handle this scenario.

.. code-block:: html

    This is text that is outside the multi-line comment.
    Online visitors can see it.

    #*
    Thus begins a multi-line comment. Online visitors won't
    see this text because the Velocity Templating Engine will
    ignore it.
    *#

    Here is text outside the multi-line comment; it is visible.

Here are a few examples to clarify how single line and multi-line comments work:

.. code-block:: html

    This text is visible. ## This text is not.
    This text is visible.
    This text is visible. #* This text, as part of a multi-line
    comment, is not visible. This text is not visible; it is also
    part of the multi-line comment. This text still not
    visible. *# This text is outside the comment, so it is visible.
    ## This text is not visible.

There is a third type of comment, the QTL comment block, which may be used to store such information as the document author and versioning information:

.. code-block:: html

    #**
    This is a QTL comment block and
    may be used to store such information
    as the document author and versioning
    information:
    @author
    @version 5
    *#
