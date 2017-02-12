flake8-import-order-spoqa
=========================

.. image:: https://img.shields.io/pypi/v/flake8-import-order-spoqa.svg
   :target: https://pypi.python.org/pypi/flake8-import-order-spoqa

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

Version 1.0.0
~~~~~~~~~~~~~

Initial release.  Released February 12, 2017.
