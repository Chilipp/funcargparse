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
