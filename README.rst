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
      - |travis| |requires| |coveralls|
    * - package
      - |version| |supported-versions| |supported-implementations|

.. |docs| image:: http://readthedocs.org/projects/funcargparse/badge/?version=latest
    :alt: Documentation Status
    :target: http://funcargparse.readthedocs.io/en/latest/?badge=latest

.. |travis| image:: https://travis-ci.org/Chilipp/funcargparse.svg?branch=master
    :alt: Travis
    :target: https://travis-ci.org/Chilipp/funcargparse

.. |coveralls| image:: https://coveralls.io/repos/github/Chilipp/funcargparse/badge.svg?branch=master
    :alt: Coverage
    :target: https://coveralls.io/github/Chilipp/funcargparse?branch=master

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
``argparse.ArgumentParser``, the ``funcargparse.FuncArgParser`` in this
package allows you to

1. automatically create a parser entirely from the docstring of a function,
   including the `help`, `metavar`, `action`, `type` and other parameters
2. Let's you chain subparsers

There are a lot of argparse extensions out there, but through the use of the
docrep_ package, this package can extract much more information to automate
the creation of the command line utility.

See the documentation_ for more information.

.. _docrep: http://docrep.readthedocs.io/en/latest/
.. _documentation: http://funcargparse.readthedocs.io/en/latest/


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
