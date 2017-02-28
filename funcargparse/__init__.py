from __future__ import print_function, division
import six
import sys
import inspect
from itertools import chain, groupby
from argparse import ArgumentParser, Namespace
import argparse
from docrep import DocstringProcessor

try:
    from cyordereddict import OrderedDict
except ImportError:
    try:
        from collections import OrderedDict
    except ImportError:
        from ordereddict import OrderedDict


if six.PY2:
    import __builtin__ as builtins
else:
    import builtins


__version__ = '0.1.2'


docstrings = DocstringProcessor()


class FuncArgParser(ArgumentParser):
    """Subclass of an argument parser that get's parts of the information
    from a given function"""

    _finalized = False

    #: The unfinished arguments after the setup
    unfinished_arguments = {}

    def __init__(self, *args, **kwargs):
        self._subparsers_action = None
        super(FuncArgParser, self).__init__(*args, **kwargs)
        self.unfinished_arguments = OrderedDict()
        self._used_functions = []
        self.__currentarg = None
        self._chain_subparsers = False
        self._setup_as = None

    @staticmethod
    def get_param_doc(doc, param):
        """Get the documentation and datatype for a parameter

        This function returns the documentation and the argument for a
        napoleon like structured docstring `doc`

        Parameters
        ----------
        doc: str
            The base docstring to use
        param: str
            The argument to use

        Returns
        -------
        str
            The documentation of the given `param`
        str
            The datatype of the given `param`"""
        arg_doc = docstrings.keep_params_s(doc, [param]) or \
            docstrings.keep_types_s(doc, [param])
        dtype = None
        if arg_doc:
            lines = arg_doc.splitlines()
            arg_doc = '\n'.join(lines[1:])
            param_desc = lines[0].split(':', 1)
            if len(param_desc) > 1:
                dtype = param_desc[1].strip()
        return arg_doc, dtype

    @docstrings.get_sectionsf('FuncArgParser.setup_args',
                              sections=['Parameters', 'Returns'])
    @docstrings.dedent
    def setup_args(self, func=None, setup_as=None, insert_at=None,
                   interprete=True):
        """
        Add the parameters from the given `func` to the parameter settings

        Parameters
        ----------
        func: function
            The function to use. If None, a function will be returned that can
            be used as a decorator
        setup_as: str
            The attribute that shall be assigned to the function in the
            resulting namespace. If specified, this function will be used when
            calling the :meth:`parse2func` method
        insert_at: int
            The position where the given `func` should be inserted. If None,
            it will be appended at the end and used when calling the
            :meth:`parse2func` method
        interprete: bool
            If True (default), the docstrings are interpreted and switches and
            lists are automatically inserted (see the
            [interpretation-docs]_

        Returns
        -------
        function
            Either the function that can be used as a decorator (if `func` is
            ``None``), or the given `func` itself.

        Examples
        --------
        Use this method as a decorator::

            >>> @parser.setup_args
            ... def do_something(a=1):
                '''
                Just an example

                Parameters
                ----------
                a: int
                    A number to increment by one
                '''
                return a + 1
            >>> args = parser.parse_args('-a 2'.split())

        Or by specifying the setup_as function::

            >>> @parser.setup_args(setup_as='func')
            ... def do_something(a=1):
                '''
                Just an example

                Parameters
                ----------
                a: int
                    A number to increment by one
                '''
                return a + 1
            >>> args = parser.parse_args('-a 2'.split())
            >>> args.func is do_something
            >>> parser.parse2func('-a 2'.split())
            3

        References
        ----------
        .. [interpretation-docs]
           http://funcargparse.readthedocs.io/en/latest/docstring_interpretation.html)
        """
        def setup(func):
            # insert the function
            if insert_at is None:
                self._used_functions.append(func)
            else:
                self._used_functions.insert(insert_at, func)

            args_dict = self.unfinished_arguments

            # save the function to use in parse2funcs
            if setup_as:
                args_dict[setup_as] = dict(
                    long=setup_as, default=func, help=argparse.SUPPRESS)
                self._setup_as = setup_as

            # create arguments
            args, varargs, varkw, defaults = inspect.getargspec(func)
            full_doc = docstrings.dedents(inspect.getdoc(func))
            if not self.description:
                summary = docstrings.get_summary(full_doc)
                if summary:
                    self.description = summary
            doc = docstrings._get_section(full_doc, 'Parameters') + '\n'
            doc += docstrings._get_section(full_doc, 'Other Parameters')
            doc = doc.rstrip()
            default_min = len(args or []) - len(defaults or [])
            for i, arg in enumerate(args):
                if arg == 'self' or arg in args_dict:
                    continue
                arg_doc, dtype = self.get_param_doc(doc, arg)
                args_dict[arg] = d = {'dest': arg, 'short': arg.replace('_',
                                                                        '-'),
                                      'long': arg.replace('_', '-')}
                if arg_doc:
                    d['help'] = arg_doc
                    if i >= default_min:
                        d['default'] = defaults[i - default_min]
                    else:
                        d['positional'] = True
                    if interprete and dtype == 'bool' and 'default' in d:
                        d['action'] = 'store_false' if d['default'] else \
                            'store_true'
                    elif interprete and dtype:
                        if dtype.startswith('list of'):
                            d['nargs'] = '+'
                            dtype = dtype[7:].strip()
                        if dtype in ['str', 'string', 'strings']:
                            d['type'] = six.text_type
                            if dtype == 'strings':
                                dtype = 'string'
                        else:
                            try:
                                d['type'] = getattr(builtins, dtype)
                            except AttributeError:
                                try:    # maybe the dtype has a final 's'
                                    d['type'] = getattr(builtins, dtype[:-1])
                                    dtype = dtype[:-1]
                                except AttributeError:
                                    pass
                        d['metavar'] = dtype
            return func
        if func is None:
            return setup
        else:
            return setup(func)

    @docstrings.get_sectionsf('FuncArgParser.add_subparsers')
    @docstrings.dedent
    def add_subparsers(self, *args, **kwargs):
        """
        Add subparsers to this parser

        Parameters
        ----------
        ``*args, **kwargs``
            As specified by the original
            :meth:`argparse.ArgumentParser.add_subparsers` method
        chain: bool
            Default: False. If True, It is enabled to chain subparsers"""
        chain = kwargs.pop('chain', None)
        ret = super(FuncArgParser, self).add_subparsers(*args, **kwargs)
        if chain:
            self._chain_subparsers = True
        self._subparsers_action = ret
        return ret

    @docstrings.dedent
    def setup_subparser(self, func=None, setup_as=None, insert_at=None,
                        interprete=True, return_parser=False, name=None,
                        **kwargs):
        """
        Create a subparser with the name of the given function

        Parameters are the same as for the :meth:`setup_args` function, other
        parameters are parsed to the :meth:`add_subparsers` method if (and only
        if) this method has not already been called.

        Parameters
        ----------
        %(FuncArgParser.setup_args.parameters)s
        return_parser: bool
            If True, the create parser is returned instead of the function
        name: str
            The name of the created parser. If None, the function name is used
            and underscores (``'_'``) are replaced by minus (``'-'``)
        ``**kwargs``
            Any other parameter that is passed to the add_parser method that
            creates the parser

        Other Parameters
        ----------------

        Returns
        -------
        FuncArgParser or %(FuncArgParser.setup_args.returns)s
            If return_parser is True, the created subparser is returned

        Examples
        --------
        Use this method as a decorator::

            >>> from funcargparser import FuncArgParser

            >>> parser = FuncArgParser()

            >>> @parser.setup_subparser
            ... def my_func(my_argument=None):
            ...     pass

            >>> args = parser.parse_args('my-func -my-argument 1'.split())
        """
        def setup(func):
            if self._subparsers_action is None:
                raise RuntimeError(
                    "No subparsers have yet been created! Run the "
                    "add_subparsers method first!")
            # replace underscore by '-'
            name2use = name
            if name2use is None:
                name2use = func.__name__.replace('_', '-')
            kwargs.setdefault('help', docstrings.get_summary(
                docstrings.dedents(inspect.getdoc(func))))
            parser = self._subparsers_action.add_parser(name2use, **kwargs)
            parser.setup_args(func, setup_as=setup_as, insert_at=insert_at,
                              interprete=interprete)
            return func, parser
        if func is None:
            return lambda f: setup(f)[0]
        else:
            return setup(func)[int(return_parser)]

    @docstrings.get_sectionsf('FuncArgParser.update_arg')
    @docstrings.dedent
    def update_arg(self, arg, if_existent=None, **kwargs):
        """
        Update the `add_argument` data for the given parameter

        Parameters
        ----------
        arg: str
            The name of the function argument
        if_existent: bool or None
            If True, the argument is updated. If None (default), the argument
            is only updated, if it exists. Otherwise, if False, the given
            ``**kwargs`` are only used if the argument is not yet existing
        ``**kwargs``
            The keyword arguments any parameter for the
            :meth:`argparse.ArgumentParser.add_argument` method
        """
        if if_existent or (if_existent is None and
                           arg in self.unfinished_arguments):
            self.unfinished_arguments[arg].update(kwargs)
        elif not if_existent and if_existent is not None:
            self.unfinished_arguments.setdefault(arg, kwargs)

    @docstrings.dedent
    def update_argf(self, arg, **kwargs):
        """
        Update the arguments as a decorator

        Parameters
        ---------
        %(FuncArgParser.update_arg.parameters)s

        Examples
        --------
        Use this method as a decorator::

            >>> from funcargparser import FuncArgParser

            >>> parser = FuncArgParser()

            >>> @parser.update_argf('my_argument', type=int)
            ... def my_func(my_argument=None):
            ...     pass

            >>> args = parser.parse_args('my-func -my-argument 1'.split())

            >>> isinstance(args.my_argument, int)
            True

        See Also
        --------
        update_arg"""
        return self._as_decorator('update_arg', arg, **kwargs)

    def _as_decorator(self, funcname, *args, **kwargs):
        def func_decorator(func):
            success = False
            for parser in self._get_corresponding_parsers(func):
                getattr(parser, funcname)(*args, **kwargs)
                success = True
            if not success:
                raise ValueError(
                    "Could not figure out to which this %s belongs" % func)
            return func
        return func_decorator

    def _get_corresponding_parsers(self, func):
        """Get the parser that has been set up by the given `function`"""
        if func in self._used_functions:
            yield self
        if self._subparsers_action is not None:
            for parser in self._subparsers_action.choices.values():
                for sp in parser._get_corresponding_parsers(func):
                    yield sp

    def pop_arg(self, *args, **kwargs):
        """Delete a previously defined argument from the parser
        """
        return self.unfinished_arguments.pop(*args, **kwargs)

    def pop_argf(self, *args, **kwargs):
        """Delete a previously defined argument from the parser via decorators

        Same as :meth:`pop_arg` but it can be used as a decorator"""
        return self._as_decorator('pop_arg', *args, **kwargs)

    def pop_key(self, arg, key, *args, **kwargs):
        """Delete a previously defined key for the `add_argument`
        """
        return self.unfinished_arguments[arg].pop(key, *args, **kwargs)

    def pop_keyf(self, *args, **kwargs):
        """Delete a previously defined key for the `add_argument`

        Same as :meth:`pop_key` but it can be used as a decorator"""
        return self._as_decorator('pop_key', *args, **kwargs)

    def create_arguments(self, subparsers=False):
        """Create and add the arguments

        Parameters
        ----------
        subparsers: bool
            If True, the arguments of the subparsers are also created"""
        ret = []
        if not self._finalized:
            for arg, d in self.unfinished_arguments.items():
                try:
                    not_positional = int(not d.pop('positional', False))
                    short = d.pop('short', None)
                    long_name = d.pop('long', None)
                    if short is None and long_name is None:
                        raise ValueError(
                            "Either a short (-) or a long (--) argument must "
                            "be provided!")
                    if not not_positional:
                        short = arg
                        long_name = None
                        d.pop('dest', None)
                    if short == long_name:
                        long_name = None
                    args = []
                    if short:
                        args.append('-' * not_positional + short)
                    if long_name:
                        args.append('--' * not_positional + long_name)
                    group = d.pop('group', self)
                    if d.get('action') in ['store_true', 'store_false']:
                        d.pop('metavar', None)
                    ret.append(group.add_argument(*args, **d))
                except Exception:
                    print('Error while creating argument %s' % arg)
                    raise
        else:
            raise ValueError('Parser has already been finalized!')
        self._finalized = True
        if subparsers and self._subparsers_action is not None:
            for parser in self._subparsers_action.choices.values():
                parser.create_arguments(True)
        return ret

    def append2help(self, arg, s):
        """Append the given string to the help of argument `arg`

        Parameters
        ----------
        arg: str
            The function argument
        s: str
            The string to append to the help"""
        self.unfinished_arguments[arg]['help'] += s

    def append2helpf(self, arg, s):
        """Append the given string to the help of argument `arg`

        Parameters
        ----------
        arg: str
            The function argument
        s: str
            The string to append to the help"""
        return self._as_decorator('append2help', arg, s)

    def grouparg(self, arg, my_arg=None, parent_cmds=[]):
        """
        Grouper function for chaining subcommands

        Parameters
        ----------
        arg: str
            The current command line argument that is parsed
        my_arg: str
            The name of this subparser. If None, this parser is the main
            parser and has no parent parser
        parent_cmds: list of str
            The available commands of the parent parsers

        Returns
        -------
        str or None
            The grouping key for the given `arg` or None if the key does
            not correspond to this parser or this parser is the main parser
            and does not have seen a subparser yet

        Notes
        -----
        Quite complicated, there is no real need to deal with this function
        """
        if self._subparsers_action is None:
            return None
        commands = self._subparsers_action.choices
        currentarg = self.__currentarg
        # the default return value is the current argument we are in or the
        # name of the subparser itself
        ret = currentarg or my_arg
        if currentarg is not None:
            # if we are already in a sub command, we use the sub parser
            sp_key = commands[currentarg].grouparg(arg, currentarg, chain(
                commands, parent_cmds))
            if sp_key is None and arg in commands:
                # if the subparser did not recognize the command, we use the
                # command the corresponds to this parser or (of this parser
                # is the parent parser) the current subparser
                self.__currentarg = currentarg = arg
                ret = my_arg or currentarg
            elif sp_key not in commands and arg in parent_cmds:
                # otherwise, if the subparser recognizes the commmand but it is
                # not in the known command of this parser, it must be another
                # command of the subparser and this parser can ignore it
                ret = None
            else:
                # otherwise the command belongs to this subparser (if this one
                # is not the subparser) or the current subparser
                ret = my_arg or currentarg
        elif arg in commands:
            # if the argument is a valid subparser, we return this one
            self.__currentarg = arg
            ret = arg
        elif arg in parent_cmds:
            # if the argument is not a valid subparser but in one of our
            # parents, we return None to signalize that we cannot categorize
            # it
            ret = None
        return ret

    def parse_known_args(self, args=None, namespace=None):
        if self._chain_subparsers:
            if args is None:
                args = sys.argv[1:]
            choices_d = OrderedDict()
            remainders = OrderedDict()
            main_args = []
            # get the first argument to make sure that everything works
            cmd = self.__currentarg = None
            for i, (cmd, subargs) in enumerate(groupby(args, self.grouparg)):
                if cmd is None:
                    main_args += list(subargs)
                else:
                    # replace '-' by underscore
                    ns_cmd = cmd.replace('-', '_')
                    choices_d[ns_cmd], remainders[ns_cmd] = super(
                        FuncArgParser, self).parse_known_args(
                            list(chain(main_args, subargs)))
            main_ns, remainders[None] = self.__parse_main(main_args)
            for key, val in vars(main_ns).items():
                choices_d[key] = val
            self.__currentarg = None
            if '__dummy' in choices_d:
                del choices_d['__dummy']
            return Namespace(**choices_d), list(chain(*remainders.values()))
        # otherwise, use the default behaviour
        return super(FuncArgParser, self).parse_known_args(args, namespace)

    def __parse_main(self, args):
        """Parse the main arguments only. This is a work around for python 2.7
        because argparse does not allow to parse arguments without subparsers
        """
        if six.PY2:
            self._subparsers_action.add_parser("__dummy")
            return super(FuncArgParser, self).parse_known_args(
                list(args) + ['__dummy'])
        return super(FuncArgParser, self).parse_known_args(args)

    @docstrings.get_sectionsf('FuncArgParser.update_short')
    @docstrings.dedent
    def update_short(self, **kwargs):
        """
        Update the short optional arguments (those with one leading '-')

        This method updates the short argument name for the specified function
        arguments as stored in :attr:`unfinished_arguments`

        Parameters
        ----------
        ``**kwargs``
            Keywords must be keys in the :attr:`unfinished_arguments`
            dictionary (i.e. keywords of the root functions), values the short
            argument names

        Examples
        --------
        Setting::

            >>> parser.update_short(something='s', something_else='se')

        is basically the same as::

            >>> parser.update_arg('something', short='s')
            >>> parser.update_arg('something_else', short='se')

        which in turn is basically comparable to::

            >>> parser.add_argument('-s', '--something', ...)
            >>> parser.add_argument('-se', '--something_else', ...)

        See Also
        --------
        update_shortf, update_long"""
        for key, val in six.iteritems(kwargs):
            self.update_arg(key, short=val)

    @docstrings.dedent
    def update_shortf(self, **kwargs):
        """
        Update the short optional arguments belonging to a function

        This method acts exactly like :meth:`update_short` but works as a
        decorator (see :meth:`update_arg` and :meth:`update_argf`)

        Parameters
        ----------
        %(FuncArgParser.update_short.parameters)s

        Returns
        -------
        function
            The function that can be used as a decorator

        Examples
        --------
        Use this method as a decorator::

            >>> @parser.update_shortf(something='s', something_else='se')
            ... def do_something(something=None, something_else=None):
            ...     ...

        See also the examples in :meth:`update_short`.

        See Also
        --------
        update_short, update_longf
        """
        return self._as_decorator('update_short', **kwargs)

    @docstrings.get_sectionsf('FuncArgParser.update_long')
    @docstrings.dedent
    def update_long(self, **kwargs):
        """
        Update the long optional arguments (those with two leading '-')

        This method updates the short argument name for the specified function
        arguments as stored in :attr:`unfinished_arguments`

        Parameters
        ----------
        ``**kwargs``
            Keywords must be keys in the :attr:`unfinished_arguments`
            dictionary (i.e. keywords of the root functions), values the long
            argument names

        Examples
        --------
        Setting::

            >>> parser.update_long(something='s', something_else='se')

        is basically the same as::

            >>> parser.update_arg('something', long='s')
            >>> parser.update_arg('something_else', long='se')

        which in turn is basically comparable to::

            >>> parser.add_argument('--s', dest='something', ...)
            >>> parser.add_argument('--se', dest='something_else', ...)

        See Also
        --------
        update_short, update_longf"""
        for key, val in six.iteritems(kwargs):
            self.update_arg(key, long=val)

    @docstrings.dedent
    def update_longf(self, **kwargs):
        """
        Update the long optional arguments belonging to a function

        This method acts exactly like :meth:`update_long` but works as a
        decorator (see :meth:`update_arg` and :meth:`update_argf`)

        Parameters
        ----------
        %(FuncArgParser.update_long.parameters)s

        Returns
        -------
        function
            The function that can be used as a decorator

        Examples
        --------
        Use this method as a decorator::

            >>> @parser.update_shortf(something='s', something_else='se')
            ... def do_something(something=None, something_else=None):
            ...     ...

        See also the examples in :meth:`update_long`.

        See Also
        --------
        update_short, update_longf
        """
        return self._as_decorator('update_long', **kwargs)

    def parse2func(self, args=None, func=None):
        """Parse the command line arguments to the setup function

        This method parses the given command line arguments to the function
        used in the :meth:`setup_args` method to setup up this parser

        Parameters
        ----------
        args: list
            The list of command line arguments
        func: function
            An alternative function to use. If None, the last function or the
            one specified through the `setup_as` parameter in the
            :meth:`setup_args` is used.

        Returns
        -------
        object
            What ever is returned by the called function

        Note
        ----
        This method does not cover subparsers!"""
        kws = vars(self.parse_args(args))
        if func is None:
            if self._setup_as:
                func = kws.pop(self._setup_as)
            else:
                func = self._used_functions[-1]
        return func(**kws)

    def parse_known2func(self, args=None, func=None):
        """Parse the command line arguments to the setup function

        This method parses the given command line arguments to the function
        used in the :meth:`setup_args` method to setup up this parser

        Parameters
        ----------
        args: list
            The list of command line arguments
        func: function or str
            An alternative function to use. If None, the last function or the
            one specified through the `setup_as` parameter in the
            :meth:`setup_args` is used.

        Returns
        -------
        object
            What ever is returned by the called function
        list
            The remaining command line arguments that could not be interpreted

        Note
        ----
        This method does not cover subparsers!"""
        ns, remainder = self.parse_known_args(args)
        kws = vars(ns)
        if func is None:
            if self._setup_as:
                func = kws.pop(self._setup_as)
            else:
                func = self._used_functions[-1]
        return func(**kws), remainder

    def parse_chained(self, args=None):
        """
        Parse the argument directly to the function used for setup

        This function parses the command line arguments to the function that
        has been used for the :meth:`setup_args`.


        Parameters
        ----------
        args: list
            The arguments parsed to the :meth:`parse_args` function

        Returns
        -------
        argparse.Namespace
            The namespace with mapping from command name to the function
            return

        See also
        --------
        parse_known_chained
        """
        kws = vars(self.parse_args(args))
        return self._parse2subparser_funcs(kws)

    def parse_known_chained(self, args=None):
        """
        Parse the argument directly to the function used for setup

        This function parses the command line arguments to the function that
        has been used for the :meth:`setup_args` method.


        Parameters
        ----------
        args: list
            The arguments parsed to the :meth:`parse_args` function

        Returns
        -------
        argparse.Namespace
            The namespace with mapping from command name to the function
            return
        list
            The remaining arguments that could not be interpreted

        See also
        --------
        parse_known
        """
        ns, remainder = self.parse_known_args(args)
        kws = vars(ns)
        return self._parse2subparser_funcs(kws), remainder

    def _parse2subparser_funcs(self, kws):
        """
        Recursive function to parse arguments to chained parsers
        """
        choices = getattr(self._subparsers_action, 'choices', {})
        replaced = {key.replace('-', '_'): key for key in choices}
        sp_commands = set(replaced).intersection(kws)
        if not sp_commands:
            if self._setup_as is not None:
                func = kws.pop(self._setup_as)
            else:
                try:
                    func = self._used_functions[-1]
                except IndexError:
                    return None
            return func(**{
                key: kws[key] for key in set(kws).difference(choices)})
        else:
            ret = {}
            for key in sp_commands:
                ret[key.replace('-', '_')] = \
                    choices[replaced[key]]._parse2subparser_funcs(
                        vars(kws[key]))
            return Namespace(**ret)

    def get_subparser(self, name):
        """
        Convenience method to get a certain subparser

        Parameters
        ----------
        name: str
            The name of the subparser

        Returns
        -------
        FuncArgParser
            The subparsers corresponding to `name`
        """
        if self._subparsers_action is None:
            raise ValueError("%s has no subparsers defined!" % self)
        return self._subparsers_action.choices[name]
