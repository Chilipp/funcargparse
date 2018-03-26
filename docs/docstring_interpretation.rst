.. currentmodule:: funcargparse

.. _docstring_interpretation:

Interpretation guidelines for docstrings
========================================

Prerequisits for the docstrings
--------------------------------
As mentioned earlier, this package uses the docrep_ package to extract the
relevant informations from the docstring. Therefore your docstrings must obey
the following rules:

1. They have to follow the `numpy conventions`_ (i.e. it should follow the
   conventions from the sphinx napoleon extension).
2. Your docstrings must either be
   :meth:`dedented <docrep.DocstringProcessor.dedent>` or start with a blank
   line.

   So this works::

       >>> def my_func(a=1):
       ...     """
       ...     Some description
       ...
       ...     Parameters
       ...     ----------
       ...     a: int
       ...         The documentation of a"""
       ...     pass

   This doesn't::

       >>> def my_func(a=1):
       ...     """Some description
       ...
       ...     Parameters
       ...     ----------
       ...     a: int
       ...         The documentation of a"""
       ...     pass

.. _docrep: http://docrep.readthedocs.io/en/latest/
.. _`numpy conventions`: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt


Default interpretations
-----------------------
To make common arguments more accessible, the :meth:`~FuncArgParser.setup_args`
method already has some preconfigured settings:

1. non-optional (e.g. ``name`` in ``def my_func(name, a=1): ...`` automatically
   get the ``'positional'`` flag. You can remove that via::

       >>> parser.pop_key('<argname>', 'positional')
2. if the default argument in the function is a boolean and the specified type
   is ``'bool'`` (e.g.::

       >>> def my_func(switch=False):
       ...     """
       ...     Some function
       ...
       ...     Parameters
       ...     ----------
       ...     switch: bool
       ...         This will be inserted as a switch
       ...     """
    The default settings for the `switch` parameter are ``action='store_true'``
    (or ``action='store_false'`` if the default value would be ``True``)
3. If the type specification in the docstring corresponds to a builtin type
   (e.g. ``'float'``, ``'int'``, ``'str'``), this type will be used to
   interprete the commandline arguments. For example::

       >>> def my_func(num=0):
       ...     """
       ...     Some function
       ...
       ...     Parameters
       ...     ----------
       ...     num: float
       ...         A floating point number
       ...     """

   will for the ``'num'`` parameter lead to the settings ``type=float``
4. If the type description starts with ``'list of'``, it will allow multiple
   arguments and interpretes everything after it as the type of it.
   For example::

       >>> def my_func(num=[1, 2, 3]):
       ...     """
       ...     Some function
       ...
       ...     Parameters
       ...     ----------
       ...     num: list of floats
       ...         Floating point numbers
       ...     """

   will lead to

   a. ``type=float``
   b. ``nargs='+'``

You can always disable the points 2-4 by setting ``interprete=False`` in the
:meth:`~FuncArgParser.setup_args` and :meth:`~FuncArgParser.setup_subparser`
call or you change the arguments by yourself by modifying the
:attr:`~FuncArgParser.unfinished_arguments` attribute, etc.


Epilog and descriptions
-----------------------
When calling the :meth:`FuncArgParser.setup_args` method or the
:meth:`FuncArgParser.setup_subparser` method, we interprete the `Notes` and
`References` methods as part of the epilog. And we interprete the description
of the function (i.e. the summary and the extended summary) as the description
of the parser. This is illustrated by this small example:

.. ipython::

    In [1]: from funcargparse import FuncArgParser

    In [2]: def do_something(a=1):
       ...:     """This is the summary and will go to the description
       ...:
       ...:     This is the extended summary and will go to the description
       ...:
       ...:     Parameters
       ...:     ----------
       ...:     a: int
       ...:         This is a parameter that will be accessible as `-a` option
       ...:
       ...:     Notes
       ...:     -----
       ...:     This section will appear in the epilog"""

    In [3]: parser = FuncArgParser(prog='do-something')

    In [4]: parser.setup_args(do_something)
       ...: parser.create_arguments()

    In [5]: parser.print_help()

Which section goes into the epilog is defined by the
:attr:`FuncArgParser.epilog_sections` attribute (specified in the
`epilog_sections` parameter of the :class:`FuncArgParser` class). By default,
we use the `Notes` and `References` section.

Also the way how the section is formatted can be specified, using the
:attr:`FuncArgParser.epilog_formatter` attribute or the
`epilog_formatter` parameter of the :class:`FuncArgParser` class. By default,
each section will be included with the section header (e.g. *Notes*) followed
by a line of hyphens (``'-'``). But you can also specify a rubric section
formatting (which would be better when being used with the sphinx-argparse_
package) or any other callable. See the following example:

.. ipython::

    In [6]: parser = FuncArgParser()
       ...: print(repr(parser.epilog_formatter))

    In [7]: parser.setup_args(do_something)
       ...: print(parser.epilog)

    # Use the bold formatter
    In [8]: parser.epilog_formatter = 'bold'
       ...: parser.setup_args(do_something, overwrite=True)
       ...: print(parser.epilog)

    # Use the rubric directive
    In [9]: parser.epilog_formatter = 'rubric'
       ...: parser.setup_args(do_something, overwrite=True)
       ...: print(parser.epilog)

    # Use a custom function
    In [10]: def uppercase_section(section, text):
       ....:     return section.upper() + '\n' + text
       ....: parser.epilog_formatter = uppercase_section
       ....: parser.setup_args(do_something, overwrite=True)
       ....: print(parser.epilog)


.. _sphinx-argparse: http://sphinx-argparse.readthedocs.io/en/latest/
