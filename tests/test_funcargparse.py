"""Test module for the :mod:`funcargparse` module.

**Disclaimer**

Copyright 2016-2019, Philipp S. Sommer

Copyright 2020-2021, Helmholtz-Zentrum Hereon

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import unittest
import six
from funcargparse import FuncArgParser, docstrings


class ParserTest(unittest.TestCase):
    """Class to test the :class:`gwgen.main.FuncArgParser` class"""

    def test_positional(self):
        """Test whether positional arguments are captured correctly"""
        def test_positional(name):
            pass
        parser = FuncArgParser()
        dtype = 'int'
        help = 'Just a dummy name'
        doc = docstrings.dedent("""
            Test function for positional argument

            Parameters
            ----------
            name: %s
                %s""" % (dtype, help))
        test_positional.__doc__ = doc
        parser.setup_args(test_positional)
        action = parser.create_arguments()[0]
        self.assertEqual(action.help.strip(), help)
        self.assertEqual(action.metavar, dtype)
        self.assertEqual(action.dest, 'name')
        self.assertEqual(action.type, int)
        self.assertTrue(action.required)

    def test_optional(self):
        """Test whether positional arguments are captured correctly"""
        default = 'test'

        def test_optional(name=default):
            pass

        parser = FuncArgParser()
        dtype = 'int'
        help = 'Just a dummy name'
        doc = docstrings.dedent("""
            Test function for positional argument

            Parameters
            ----------
            name: %s
                %s""" % (dtype, help))
        test_optional.__doc__ = doc
        parser.setup_args(test_optional)
        action = parser.create_arguments()[0]
        self.assertEqual(action.help.strip(), help)
        self.assertEqual(action.metavar, dtype)
        self.assertEqual(action.dest, 'name')
        self.assertEqual(action.type, int)
        self.assertTrue(action.default, default)

    def test_switch(self):
        """Test whether switches are captured correctly"""
        def test_switch(name=False):
            pass
        parser = FuncArgParser()
        dtype = 'bool'
        help = 'Just a dummy name'
        doc = docstrings.dedent("""
            Test function for positional argument

            Parameters
            ----------
            name: %s
                %s""" % (dtype, help))
        test_switch.__doc__ = doc
        parser.setup_args(test_switch)
        action = parser.create_arguments()[0]
        self.assertEqual(action.help.strip(), help)
        self.assertIsNone(action.metavar)
        self.assertEqual(action.dest, 'name')
        self.assertFalse(action.default)
        self.assertTrue(action.const)

    def test_subparser_chain(self):
        '''Test whether the subparser chaining works'''
        parser = FuncArgParser()
        parser.add_argument('-a')
        sps = parser.add_subparsers(chain=True)
        # first subparser
        sp1 = sps.add_parser('sp1')
        sp1.add_argument('-t', action='store_false')
        sps1 = sp1.add_subparsers(chain=True)

        # subparsers of first subparser (second level)
        sp11 = sps1.add_parser('sp11')
        sp11.add_argument('-b')
        sp12 = sps1.add_parser('sp12')
        sp12.add_argument('-c', action='store_true')

        # second subparser
        sp2 = sps.add_parser('sp2')
        sp2.add_argument('-t', action='store_false')

        args = parser.parse_args(
            '-a test sp1 -t sp11 -b okay sp12 -c sp2'.split())
        # first level test
        self.assertTrue(args.a, 'test')
        self.assertTrue(args.sp1.a, 'test')
        self.assertTrue(args.sp2.a, 'test')
        self.assertFalse(args.sp1.t)
        self.assertTrue(args.sp2.t)

        # second level test
        self.assertFalse(args.sp1.sp11.t)
        self.assertFalse(args.sp1.sp12.t)
        self.assertEqual(args.sp1.sp11.b, 'okay')
        self.assertTrue(args.sp1.sp12.c)

    def test_argument_modification(self):
        """Test the modification of arguments"""

        def test(name='okay', to_delete=True):
            '''
            That's a test function

            Parameters
            ----------
            name: str
                Just a test
            to_delete: bool
                A parameter that will be deleted

            Returns
            -------
            NoneType
                Nothing'''
        parser = FuncArgParser()
        parser.setup_args(test)
        parser.update_arg('name', help='replaced', metavar='replaced')

    def test_subparser_renamed(self):
        """Test whether one can use the same argument for a subparser again"""
        parser = FuncArgParser()
        parser.add_argument('-a')
        sps = parser.add_subparsers(chain=True)
        # first subparser
        sp1 = sps.add_parser('sp1')
        sp1.add_argument('-t', action='store_false')
        sps1 = sp1.add_subparsers(chain=False)

        # Add a parser with the same name as the following subparser
        sp11_root = sps.add_parser('sp11')
        sp11_root.add_argument('-b')

        # subparsers of first subparser (second level)
        sp11 = sps1.add_parser('sp11')
        sp11.add_argument('-b')
        sp12 = sps1.add_parser('sp12')
        sp12.add_argument('-c', action='store_true')

        # second subparser
        sp2 = sps.add_parser('sp2')
        sp2.add_argument('-t', action='store_false')
        args = parser.parse_args(
            '-a test sp11 -b root sp1 -t sp11 -b okay sp2'.split())
        self.assertEqual(args.sp1.b, 'okay')
        self.assertEqual(args.sp11.b, 'root')

    def test_subparser_renamed_chain(self):
        """Test whether one can use the same argument for a subparser again
        with chain"""
        parser = FuncArgParser()
        parser.add_argument('-a')
        sps = parser.add_subparsers(chain=True)
        # first subparser
        sp1 = sps.add_parser('sp1')
        sp1.add_argument('-t', action='store_false')
        sps1 = sp1.add_subparsers(chain=True)

        # Add a parser with the same name as the following subparser
        sp11_root = sps.add_parser('sp11')
        sp11_root.add_argument('-b')

        # subparsers of first subparser (second level)
        sp11 = sps1.add_parser('sp11')
        sp11.add_argument('-b')
        sp12 = sps1.add_parser('sp12')
        sp12.add_argument('-c', action='store_true')

        # second subparser
        sp2 = sps.add_parser('sp2')
        sp2.add_argument('-t', action='store_false')
        args = parser.parse_args(
            '-a test sp11 -b root sp1 -t sp11 -b okay sp12 -c sp2'.split())
        self.assertEqual(args.sp1.sp11.b, 'okay')
        self.assertEqual(args.sp11.b, 'root')

    def test_update(self):
        """Test whether the arguments are updated correctly"""
        def test_switch(name=False, name2=True):
            pass
        parser = FuncArgParser()
        dtype = 'bool'
        help = 'Just a dummy name'
        doc = docstrings.dedent("""
            Test function for positional argument

            Parameters
            ----------
            name: %s
                Anything""" % (dtype))
        test_switch.__doc__ = doc
        parser.setup_args(test_switch)
        parser.update_arg('name', help=help)
        parser.update_arg('test', help=help, if_existent=False)
        self.assertEqual(parser.unfinished_arguments['name']['help'], help)
        self.assertIn('test', parser.unfinished_arguments)
        self.assertEqual(parser.unfinished_arguments['test']['help'], help)

        parser.update_arg('test2', help=help)
        self.assertNotIn('test2', parser.unfinished_arguments)

        if six.PY3:
            with self.assertRaises(KeyError):
                parser.update_arg('test3', if_existent=True, help=help)

    def test_list_of(self):
        """Test whether arguments with list of are converted correctly"""
        def test_func(name=None, name2=None):
            """
            Test function for positional argument

            Parameters
            ----------
            name: list of floats
                Anything
            name2: list of int
                Anything else"""
            pass

        parser = FuncArgParser()
        parser.setup_args(test_func)
        d = parser.unfinished_arguments
        # test list of floats
        self.assertEqual(d['name']['nargs'], '+')
        self.assertEqual(d['name']['metavar'], 'float')
        self.assertEqual(d['name']['type'], float)

        # test list of int
        self.assertEqual(d['name2']['nargs'], '+')
        self.assertEqual(d['name2']['metavar'], 'int')
        self.assertEqual(d['name2']['type'], int)

    def test_dtypes(self):
        """Test whether arguments with list of are converted correctly"""
        def test_func(name=None, name2=None, name3=2):
            """
            Test function for positional argument

            Parameters
            ----------
            name: float
                Anything
            name2: list of strings
                Anything else
            name3: anything
                Something with unknown dtype"""
            pass

        parser = FuncArgParser()
        parser.setup_args(test_func)
        d = parser.unfinished_arguments
        # test builtin float
        self.assertEqual(d['name']['type'], float)

        # test strings
        self.assertEqual(d['name2']['type'], six.text_type)

        # test unknown type
        self.assertNotIn('type', d['name3'])

    def test_parse2func(self):
        """Test whether the parsing to functions works"""
        # test setup with one function
        parser = FuncArgParser()

        @parser.setup_args
        def test_func(a=1):
            """
            Test function for positional argument

            Parameters
            ----------
            a: float
                The number to increment by 1"""
            return a + 1

        parser.create_arguments()

        self.assertEqual(parser.parse2func('-a 2'.split()), 3)
        self.assertEqual(parser.parse_known2func('-a 2'.split())[0], 3)

        # test setup after 2 functions
        parser = FuncArgParser()

        def test_func2(a=1):
            return a + 2

        test_func2.__doc__ = test_func.__doc__

        parser.setup_args(test_func2, setup_as='func')
        parser.setup_args(test_func)

        parser.create_arguments()

        self.assertEqual(parser.parse2func('-a 2'.split()), 4)
        self.assertEqual(parser.parse_known2func('-a 2'.split())[0], 4)
        self.assertIs(parser.parse_args('-a 2'.split()).func, test_func2)

    def test_parse_chained(self):
        """Test whether the parsing to chained function works"""

        parser = FuncArgParser()

        parser.add_subparsers(chain=True)

        @parser.setup_subparser(setup_as='func')
        def test_1():
            return 'test1 okay'

        @parser.setup_subparser
        def test_2():
            return 'test2 okay'

        parser.create_arguments(True)

        ns = parser.parse_chained('test-1 test-2'.split())

        self.assertEqual(ns.test_1, 'test1 okay')
        self.assertEqual(ns.test_2, 'test2 okay')

        ns = parser.parse_known_chained('test-1 test-2'.split())[0]

        self.assertEqual(ns.test_1, 'test1 okay')
        self.assertEqual(ns.test_2, 'test2 okay')

    def test_decorators(self):
        """Test whether the decorator methodology works"""
        parser = FuncArgParser()

        sps = parser.add_subparsers()
        sp = sps.add_parser('test')

        @parser.append2helpf('a', '. Default: %(default)s')
        @parser.pop_keyf('a', 'metavar')
        @parser.update_shortf(a='n')
        @parser.update_longf(a='something')
        @parser.update_argf('a', type=int)
        @parser.pop_argf('b')
        @sp.setup_args(insert_at=0)
        def test_func(a=1, b=2):
            """
            Test function for positional argument

            Parameters
            ----------
            a: float
                The number to increment by 1
            b: float
                Another number"""
            return a + b

        self.assertNotIn('b', sp.unfinished_arguments)
        self.assertEqual(sp.unfinished_arguments['a']['long'], 'something')
        self.assertEqual(sp.unfinished_arguments['a']['short'], 'n')
        self.assertIs(sp.unfinished_arguments['a']['type'], int)
        self.assertNotIn('metavar', sp.unfinished_arguments['a'])
        self.assertIn('Default:', sp.unfinished_arguments['a']['help'])

    def test_epilog(self):
        """Test whether the epilog is extracted correctly"""
        heading = 'Notes\n-----'
        content = 'should be included in the parser epilog'
        epilog = heading + '\n' + content

        @docstrings.dedent
        def test_func(a=1):
            """Test function

            Parameters
            ----------
            a: int
                A parameter"""

        test_func.__doc__ += '\n\n' + epilog

        # test standard heading formatter
        parser = FuncArgParser()
        parser.setup_args(test_func)

        self.assertEqual(parser.epilog, epilog)

        # test bold formatter
        parser = FuncArgParser(epilog_formatter='bold')
        parser.setup_args(test_func)

        self.assertEqual(parser.epilog, '**Notes**' + '\n\n' + content)

        # test rubric formatter
        parser = FuncArgParser(epilog_formatter='rubric')
        parser.setup_args(test_func)

        self.assertEqual(parser.epilog, '.. rubric:: Notes' + '\n\n' + content)

        def formatter(section, text):
            return section + text

        # test function formatter
        parser = FuncArgParser(epilog_formatter=formatter)
        parser.setup_args(test_func)

        self.assertEqual(parser.epilog, 'Notes' + content)

        # test appending
        parser.setup_args(test_func)
        self.assertEqual(parser.epilog, '\n\n'.join(['Notes' + content] * 2))

        # test overwrite
        parser.setup_args(test_func, overwrite=True)
        self.assertEqual(parser.epilog, 'Notes' + content)


if __name__ == '__main__':
    unittest.main()
