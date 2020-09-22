v0.2.3
======
Minor patch for docrep 0.3

v0.2.2
======
Minor patch to use ``inspect.getfullargspec`` instead of ``inspect.getargspec``
because the latter has been deprecated in python 3.0

v0.2.1
======
Small patch to use ``inspect.cleandoc`` instead of ``docrep.dedents``

v0.2.0
======
This release just adds some new interpretation features to extract the
parser description and the epilog from the parsed function. They might
changed how your parser looks drastically!

Changed
-------
* The default formatter_class for the :class:`FuncArgParser` is now the
  :class:`argparse.RawHelpFormatter`, which makes sense since we expect that
  the documentations are already nicely formatted
* When calling the :meth:`FuncArgParser.setup_args` method, we also look for
  the *Notes* and *References* sections which will be included in the epilog
  of the parser. If you want to disable this feature, just initialize the
  parser with::

      parser = FuncArgParser(epilog_sections=[])

  This feature might cause troubles when being used in sphinx documentations
  in conjunction with the sphinx-argparse_ package. For this, you can change
  the formatting of the heading with the :attr:`FuncArgParser.epilog_formatter`
  attribute

.. _sphinx-argparse: http://sphinx-argparse.readthedocs.io/en/latest/

Added
-----
* Changelog
