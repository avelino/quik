==========
User Guide
==========


About this Guide
================

The Quik User Guide is intended to help page designers and content providers get acquainted with Quik and the syntax of its simple yet powerful scripting language, the Quik Template Language (QTL). Many of the examples in this guide deal with using Quik to embed dynamic content in web sites, but all QTL examples are equally applicable to other pages and templates.

Thanks for choosing Quik!


Hello Quik World!
=================

Once a value has been assigned to a variable, you can reference the variable anywhere in your HTML document. In the following example, a value is assigned to @foo and later referenced.

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
    see this text because the Quik Templating Engine will
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


References
==========

There are three types of references in the QTL: variables, properties and methods. As a designer using the QTL, you and your engineers must come to an agreement on the specific names of references so you can use them correctly in your templates.

Everything coming to and from a reference is treated as a String object. If there is an object that represents *@foo* (such as an Integer object), then Quik will call its **.toString()** method to resolve the object into a String.

Variables
---------

The shorthand notation of a variable consists of a leading "@" character followed by a QTL Identifier. A QTL Identifier must start with an alphabetic character (a .. z or A .. Z). The rest of the characters are limited to the following types of characters:

- alphabetic (a .. z, A .. Z)
- numeric (0 .. 9)
- hyphen ("-")
- underscore ("_")

Here are some examples of valid variable references in the QTL:

.. code-block:: html

    @foo
    @mudSlinger
    @mud-slinger
    @mud_slinger
    @mudSlinger1

When QTL references a variable, such as @foo, the variable can get its value from either a set directive in the template, or from the Python code. For example, if the Java variable @foo has the value bar at the time the template is requested, bar replaces all instances of @foo on the web page. Alternatively, if I include the statement

.. code-block:: html

    #set( @foo = "bar" )


The output will be the same for all instances of @foo that follow this directive.

Properties
----------

The second flavor of QTL references are properties, and properties have a distinctive format. The shorthand notation consists of a leading @ character followed a QTL Identifier, followed by a dot character (".") and another QTL Identifier. These are examples of valid property references in the QTL:

.. code-block:: html

    @customer.Address
    @purchase.Total

Take the first example, @customer.Address. It can have two meanings. It can mean, Look in the hashtable identified as customer and return the value associated with the key Address. But @customer.Address can also be referring to a method (references that refer to methods will be discussed in the next section); @customer.Address could be an abbreviated way of writing @customer.getAddress(). When your page is requested, Quik will determine which of these two possibilities makes sense, and then return the appropriate value.

Formal Reference Notation
-------------------------

Shorthand notation for references was used for the examples listed above, but there is also a formal notation for references, which is demonstrated below:

.. code-block:: html

    @{mudSlinger}
    @{customer.Address}

In almost all cases you will use the shorthand notation for references, but in some cases the formal notation is required for correct processing.

Suppose you were constructing a sentence on the fly where @vice was to be used as the base word in the noun of a sentence. The goal is to allow someone to choose the base word and produce one of the two following results: "Avelino is a Pythonmaniac." or "Avelino is a Developermaniac.". Using the shorthand notation would be inadequate for this task. Consider the following example:

.. code-block:: html

    Avelino is a @vicemaniac.

There is ambiguity here, and Quik assumes that @vicemaniac, not @vice, is the Identifier that you mean to use. Finding no value for @vicemaniac, it will return @vicemaniac. Using formal notation can resolve this problem.

.. code-block:: html

    Avelino is a @{vice}maniac.

Now Quik knows that @vice, not @vicemaniac, is the reference. Formal notation is often useful when references are directly adjacent to text in a template.

Quiet Reference Notation
------------------------

When Quik encounters an undefined reference, its normal behavior is to output the image of the reference. For example, suppose the following reference appears as part of a QTL template.

.. code-block:: html

    <input type="text" name="email" value="@email"/>

When the form initially loads, the variable reference @email has no value, but you prefer a blank text field to one with a value of "@email". Using the quiet reference notation circumvents Velocity's normal behavior; instead of using @email in the QTL you would use !@email. So the above example would look like the following:

.. code-block:: html

    <input type="text" name="email" value="@!email"/>

Now when the form is initially loaded and @email still has no value, an empty string will be output instead of "@email".

Formal and quiet reference notation can be used together, as demonstrated below.

.. code-block:: html

    <input type="text" name="email" value="@!{email}"/>
