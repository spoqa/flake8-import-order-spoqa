flake8-import-order-spoqa
=========================

.. image:: https://img.shields.io/pypi/v/flake8-import-order-spoqa.svg
   :target: https://pypi.org/project/flake8-import-order-spoqa/

.. image:: https://travis-ci.org/spoqa/flake8-import-order-spoqa.svg
   :target: https://travis-ci.org/spoqa/flake8-import-order-spoqa

This extends flake8-import-order_ to implement Spoqa's import order convention.
It bascially follows PEP 8 with our some additional rules:

-  Standard libraries shouldn't be imported using ``from ... import ...``
   statement.  It's because standard libraries tend to use general terms
   like ``open``.  We instead use always qualified imports to eliminate
   name pollution:

   .. code-block:: python

      import sys  # Yes

      from sys import version_info  # No

   However, there are few exceptions like ``typing`` module.  They can be
   imported in both ways:

   .. code-block:: python

      import typing
      from typing import Optional  # `from ... import ...` must be latter

-  All other than standard libraries should be imported using
   ``from ... import ...`` statement:

   .. code-block:: python

      from flask import Flask  # Yes

      import flask  # No

-  Deeper relative imports should go former.  This rule makes consistent
   even when relative imports are rewritten as absolute imports.

   .. code-block:: python

      from ..deeper import former
      from ...deepest import later

-  Imported names are splited to three categories:  ``CONSTANT_NAME``,
   ``ClassName``, and ``normal_names``, and follow that order:

   .. code-block:: python

      from something import CONST_A, CONST_B, ClassA, ClassB, any_func, any_var

.. _flake8-import-order: https://github.com/PyCQA/flake8-import-order


Usage
-----

Install the ``flake8-import-order-spoqa`` using pip_, and then specify
``--import-order-style=spoqa`` option.  Or you can specify it on the config_
file as well:

.. code-block:: ini

   [flake8]
   import-order-style = spoqa

Because `runtime extensible styles`__ is introduced__ from
flake-import-order 0.12, you need to install flake-import-order 0.12 or later.

.. _pip: http://pip-installer.org/
.. _config: http://flake8.pycqa.org/en/latest/user/configuration.html
__ https://github.com/PyCQA/flake8-import-order#extending-styles
__ https://github.com/PyCQA/flake8-import-order/pull/103


Distribution
------------

Written by `Hong Minhee`__, and distributed under GPLv3_ or later.

__ https://hongminhee.org/
.. _GPLv3: https://www.gnu.org/licenses/gpl-3.0.html


Changelog
---------

Version 1.4.0
~~~~~~~~~~~~~

Released on May 22, 2018.

- Python 3.3 became no more supported.


Version 1.3.0
~~~~~~~~~~~~~

Released on February 12, 2018.

- Older versions than flake8-import-order 0.17 are now unsupported.
  (Under the hood, since flake8-import-order 0.17 refactored their internals
  so that constants like ``IMPORT_3RD_PARTY``, ``IMPORT_APP``,
  ``IMPORT_APP_PACKAGE``, ``IMPORT_APP_RELATIVE``, and ``IMPORT_STDLIB``
  are evolved to ``ImportType`` enum type, flake8-import-order-spoqa also
  became to follow that.)  [`#3`_]

.. _#3: https://github.com/spoqa/flake8-import-order-spoqa/issues/3


Version 1.2.0
~~~~~~~~~~~~~

Released on November 27, 2017.

- Older versions than flake8-import-order 0.16 are now unsupported.
  (Under the hood, since flake8-import-order 0.16 refactored their internals
  so that no more ``Style.check()`` method and ``Style.imports`` property
  exist, flake8-import-order-spoqa also became to follow that.)


Version 1.1.0
~~~~~~~~~~~~~

Released on October 31, 2017.

- Older versions than flake8-import-order 0.14.2 are now unsupported.


Version 1.0.2
~~~~~~~~~~~~~

Released on October 31, 2017.

- Fixed incompatibility with flake8-import-order 0.14.1 or higher.


Version 1.0.1
~~~~~~~~~~~~~

Released on July 15, 2017.

- Fixed a bug that wrong order of names (e.g. ``from ... import second, first``)
  had been not warned.


Version 1.0.0
~~~~~~~~~~~~~

Initial release.  Released on February 12, 2017.
