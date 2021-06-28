.. funcargparse documentation master file

==========================================================
Create an argparse.ArgumentParser from function docstrings
==========================================================

.. start-badges

.. list-table::
    :stub-columns: 1
    :widths: 10 90

    * - docs
      - |docs|
    * - tests
      - |github-action| |requires| |codecov|
    * - package
      - |version| |supported-versions| |supported-implementations|

.. |docs| image:: http://readthedocs.org/projects/funcargparse/badge/?version=latest
    :alt: Documentation Status
    :target: http://funcargparse.readthedocs.io/en/latest/?badge=latest

.. |github-action| image:: https://github.com/Chilipp/funcargparse/workflows/Tests/badge.svg
    :alt: Tests
    :target: https://github.com/Chilipp/funcargparse/actions?query=workflow%3A%22Tests%22

.. |codecov| image:: https://codecov.io/gh/Chilipp/funcargparse/branch/master/graph/badge.svg?token=UX1B5ocBbP
    :alt: Codecov
    :target: https://codecov.io/gh/Chilipp/funcargparse

.. |requires| image:: https://requires.io/github/Chilipp/funcargparse/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/Chilipp/funcargparse/requirements/?branch=master

.. |version| image:: https://img.shields.io/pypi/v/funcargparse.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/funcargparse

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/funcargparse.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/funcargparse

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/funcargparse.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/funcargparse


.. end-badges


Welcome! Additionally to the default behaviour of the
:class:`argparse.ArgumentParser`, the :class:`funcargparse.FuncArgParser`
allows you to

1. automatically create a parser entirely from the docstring of a function,
   including the `help`, `metavar`, `action`, `type` and other parameters
2. Let's you :ref:`chain subparsers <chain_subparsers>`

There are a lot of argparse extensions out there, but through the use of the
docrep_ package, this package can extract much more information to automate
the creation of the command line utility.

See :ref:`getting_started` for more information.

.. _docrep: http://docrep.readthedocs.io/en/latest/

Content
-------

.. toctree::
    :maxdepth: 1

    getting_started
    docstring_interpretation
    api/funcargparse
    changelog


.. _install:

Installation
============

Simply install it via ``pip``::

    $ pip install funcargparse

Or you install it via::

    $ python setup.py install

from the `source on GitHub`_.

.. _source on GitHub: https://github.com/Chilipp/funcargparse


Requirements
============
The package only requires the docrep_ package which we use under the hood to
extract the necessary parts from the docstrings.

The package has been tested for python 2.7 and 3.5.

.. _docrep: http://docrep.readthedocs.io/en/latest/


Disclaimer
==========

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


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
