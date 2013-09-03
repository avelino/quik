quik
====

A fast and lightweight Python template engine


Nutshell
--------

Here a small example of a Quik template::

    <ul>
        #for ($user in $users)
            #if($user.age > 18)
            <li><a href="$user.url">$user.username</a></li>
            #end
        #end
    </ul>


Features
--------

- Easy to use.
- High performance.
- Autoescaping.
- Template inheritance.
- Supports native python expressions.
