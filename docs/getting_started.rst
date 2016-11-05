.. currentmodule:: funcargparse

.. _getting_started:


Getting started
===============

Motivation
----------

Suppose we want a simple script that adds or multiplies two numbers. This code
should then be

1. callable inside python (i.e. we create a function)
2. executable from the command line

So let's setup the function in a file called ``'add_or_multiply.py'`` like this

.. ipython::

    In [1]: def do_something(a, b, multiply=False):
       ...:    """
       ...:    Multiply or add one number to the others
       ...:
       ...:    Parameters
       ...:    ----------
       ...:    a: int
       ...:        Number 1
       ...:    b: list of int
       ...:        A list of numbers to add `a` to
       ...:    multiply: bool
       ...:        If True, the numbers are multiplied, not added
       ...:    """
       ...:    if multiply:
       ...:        result = [n * a for n in b]
       ...:    else:
       ...:        result = [n + a for n in b]
       ...:    print(result)

Now, if you want to make a command line script out of it, the usual methodology
is to create an :class:`argparse.ArgumentParser` instance and parse the
arguments like this

.. ipython::

    @verbatim
    In [2]: if __name__ == '__main__':
       ...:     from argparse import ArgumentParser
       ...:     parser = ArgumentParser(
       ...:         description='Multiply or add two numbers')
       ...:     parser.add_argument('a', type=int, help='Number 1')
       ...:     parser.add_argument('b', type=int, nargs='+',
       ...:                         help='A list of numbers to add `a` to')
       ...:     parser.add_argument('-m', '--multiply', action='store_true',
       ...:                         help='Multiply the numbers instead of adding them')
       ...:     args = parser.parse_args('3 2 -m'.split())
       ...:     do_something(**vars(args))
       ...:

    @suppress
    In [3]:     from argparse import ArgumentParser
       ...:     parser = ArgumentParser(
       ...:         description='Multiply or add two numbers')
       ...:     parser.add_argument('a', type=int, help='Number 1')
       ...:     parser.add_argument('b', type=int, nargs='+',
       ...:                         help='A list of numbers to add `a` to')
       ...:     parser.add_argument('-m', '--multiply', action='store_true',
       ...:                         help='Multiply the numbers instead of adding them')

Now, if you parse the arguments, you get

.. ipython::

    In [3]: parser.print_help()

However, you could skip the entire lines above, if you just use the
:class:`funcargparse.FuncArgParser`

.. ipython::

    In [4]: from funcargparse import FuncArgParser

    In [5]: parser = FuncArgParser()

    In [6]: parser.setup_args(do_something)

    In [7]: parser.update_short(multiply='m')

    In [8]: actions = parser.create_arguments()

    In [9]: parser.print_help()

    @suppress
    In [9]: del parser

or you use the parser right in the beginning as a decorator

.. ipython::

    @suppress
    In [10]: parser = FuncArgParser()

    In [10]: @parser.update_shortf(multiply='m')
       ....: @parser.setup_args
       ....: def do_something(a, b, multiply=False):
       ....:    """
       ....:    Multiply or add one number to the others
       ....:
       ....:    Parameters
       ....:    ----------
       ....:    a: int
       ....:        Number 1
       ....:    b: list of int
       ....:        A list of numbers to add `a` to
       ....:    multiply: bool
       ....:        If True, the numbers are multiplied, not added
       ....:    """
       ....:    if multiply:
       ....:        result = [n * a for n in b]
       ....:    else:
       ....:        result = [n + a for n in b]
       ....:    print(result)

    In [13]: actions = parser.create_arguments()

    In [12]: parser.print_help()

The :class:`FuncArgParser` interpretes the docstring
(see :ref:`docstring_interpretation`) and sets up the arguments.

Your ``'__main__'`` part could then simply look like

.. ipython::

    @verbatim
    In [11]: if __name__ == '__main__':
       ....:     parser.parse_to_func()

.. _usage:

Usage
-----
Generally the usage is

1. create an instance of the :class:`FuncArgParser` class
2. setup the arguments using the :meth:`~FuncArgParser.setup_args` function
3. modify the arguments (optional) either

   a. in the :attr:`FuncArgParser.unfinished_arguments` dictionary
   b. using the :meth:`~FuncArgParser.update_arg`,
      :meth:`~FuncArgParser.update_short`, :meth:`~FuncArgParser.update_long` or
      :meth:`~FuncArgParser.append2help` methods
   c. using the equivalent decorator methods :meth:`~FuncArgParser.update_argf`,
      :meth:`~FuncArgParser.update_shortf`, :meth:`~FuncArgParser.update_longf` or
      :meth:`~FuncArgParser.append2helpf`

4. create the arguments using the :meth:`~FuncArgParser.create_arguments`
   method

.. _subparsers:

Subparsers
----------
You can also use subparsers for controlling you program (see the
:meth:`argparse.ArgumentParser.add_subparsers` method). They can either be
implemented the classical way via

.. ipython::

    @suppress
    In [12]: parser = FuncArgParser()

    In [12]: subparsers = parser.add_subparsers()

    In [13]: subparser = subparsers.add_parser('test')

And then as with the parent parser you can use function docstrings.

.. ipython::

    In [14]: @subparser.setup_args
       ....: def my_other_func(b=1):
       ....:     """
       ....:     Subparser summary
       ....:
       ....:     Parameters
       ....:     ----------
       ....:     b: int
       ....:         Anything"""
       ....:     print(b * 500)

    In [15]: subparser.create_arguments()

    In [16]: parser.print_help()

On the other hand, you can use the :meth:`~FuncArgParser.setup_subparser`
method to directly create the subparser

.. ipython::

    @suppress
    In [14]: parser = FuncArgParser()

    In [15]: parser.add_subparsers()

    In [16]: @parser.setup_subparser
       ....: def my_other_func(b=1):
       ....:     """
       ....:     Subparser summary
       ....:
       ....:     Parameters
       ....:     ----------
       ....:     b: int
       ....:         Anything"""
       ....:     print(b * 500)

    In [17]: parser.create_arguments(subparsers=True)

    In [18]: parser.print_help()

which now created the ``my-other-func`` sub command.

.. _chain_subparsers:

Chaining subparsers
-------------------
Separate from the usage of the function docstring, we implemented the
possibilty to chain subparsers. This changes the handling of subparsers
compared to the default behaviour (which is inherited from the
:class:`argparse.ArgumentParser`). The difference can be shown in the following
example

.. ipython::

    In [19]: from argparse import ArgumentParser

    In [20]: argparser = ArgumentParser()

    In [21]: funcargparser = FuncArgParser()

    In [22]: sps_argparse = argparser.add_subparsers()

    In [23]: sps_funcargparse = funcargparser.add_subparsers(chain=True)

    In [24]: sps_argparse.add_parser('dummy').add_argument('-a')

    In [25]: sps_funcargparse.add_parser('dummy').add_argument('-a')

    In [26]: ns_default = argparser.parse_args('dummy -a 3'.split())

    In [27]: ns_chained = funcargparser.parse_args('dummy -a 3'.split())

    In [28]: print(ns_default, ns_chained)

So while the default behaviour is, to put the arguments in the main namespace
like

.. ipython::

    In [29]: ns_default.a

the chained subparser procedure puts the commands for the ``'dummy'`` command
into an extra namespace like

.. ipython::

    In [30]: ns_chained.dummy.a

This has the advantages that we don't mix up subparsers if we chain them. So
here is an example demonstrating the power of it

.. ipython::
    :okexcept:

    In [31]: sps_argparse.add_parser('dummy2').add_argument('-a')

    In [32]: sps_funcargparse.add_parser('dummy2').add_argument('-a')

    # with allowing chained subcommands, we get
    In [33]: ns_chained = funcargparser.parse_args('dummy -a 3 dummy2 -a 4'.split())

    In [34]: print(ns_chained.dummy.a, ns_chained.dummy2.a)

    # on the other side, the default ArgumentParser raises an error because
    # chaining is not allowed
    In [35]: ns_default = argparser.parse_args('dummy -a 3 dummy2 -a 4'.split())

Furthermore, you can use the :meth:`~FuncArgParser.parse_chained` and the
:meth:`~FuncArgParser.parse_known_chained` methods to parse directly to the
subparsers.

.. ipython::

    In [36]: parser = FuncArgParser()

    In [37]: sps = parser.add_subparsers(chain=True)

    In [38]: @parser.setup_subparser
       ....: def subcommand_1():
       ....:     print('Calling subcommand 1')
       ....:     return 1

    In [39]: @parser.setup_subparser
       ....: def subcommand_2():
       ....:    print('Calling subcommand 2')
       ....:    return 2

    In [40]: parser.create_arguments(True)

    In [41]: parser.parse_chained('subcommand-1 subcommand-2'.split())


.. warning::

    If you reuse an already existing command in the subcommand of another
    subcommand, the latter one get's prefered. See this example

    .. ipython::

        In [42]: sp = sps.add_parser('subcommand-3')

        In [43]: sps1 = sp.add_subparsers(chain=True)

        # create the same subparser subcommand-1 but as a subcommand of the
        # subcommand-3 subparser
        In [44]: @sp.setup_subparser
           ....: def subcommand_1():
           ....:     print('Calling modified subcommand 1')
           ....:     return 3.1

        In [45]: sp.create_arguments(True)

        # subcommand-1 get's called
        In [46]: parser.parse_chained('subcommand-1 subcommand-3'.split())

        # subcommand-3.subcommand-1 get's called
        In [47]: parser.parse_chained('subcommand-3 subcommand-1'.split())
