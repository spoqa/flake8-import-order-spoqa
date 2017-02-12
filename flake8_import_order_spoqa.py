import ast
import textwrap
import unittest

from flake8_import_order import (IMPORT_3RD_PARTY, IMPORT_APP,
                                 IMPORT_APP_PACKAGE, IMPORT_APP_RELATIVE,
                                 IMPORT_STDLIB)
from flake8_import_order.checker import ImportOrderChecker
from flake8_import_order.styles import Error, Style, lookup_entry_point

__all__ = 'Spoqa',


class Spoqa(Style):

    from_importable_standard_librarires = frozenset(['typing'])

    @staticmethod
    def name_key(identifier):
        name = identifier.lstrip('_')
        hidden = name != identifier
        if not name:
            return 2, hidden
        elif name.isupper():
            return 0, hidden  # constants e.g. CONSTANT_NAME
        elif name[0].isupper():
            return 1, hidden  # classes e.g. ClassName
        else:
            return 2, hidden  # normal variables e.g. normal_names

    @staticmethod
    def module_key(name):
        return name.lower(), name

    @classmethod
    def sorted_names(cls, names):
        return sorted(names, key=cls.name_key)

    @classmethod
    def import_key(cls, import_):
        modules = [cls.module_key(module) for module in import_.modules]
        names = [cls.name_key(name) for name in import_.names]
        group = import_.type
        if group in (IMPORT_APP, IMPORT_APP_PACKAGE):
            group += IMPORT_APP_RELATIVE
        return group, -import_.level, modules, names

    def check(self):
        for i in self.imports:
            mod = i.modules[0]
            if i.type == IMPORT_STDLIB and i.is_from and \
               mod not in self.from_importable_standard_librarires:
                yield Error(i.lineno, 'I901',
                            'A standard library is imported using '
                            '"from {0} import ..." statement. Should be '
                            '"import {0}" instead.'.format(mod))
            elif i.type == IMPORT_3RD_PARTY and not i.is_from:
                yield Error(i.lineno, 'I902',
                            'A third party library is imported using '
                            '"import {0}" statement. Should be '
                            '"from {0} import ..." instead.'.format(mod))
            elif i.type in (IMPORT_APP, IMPORT_APP_PACKAGE) and not i.is_from:
                yield Error(i.lineno, 'I902',
                            'An app module is imported using "import {0}"'
                            ' statement. Should be "from {0} import ..."'
                            ' instead.'.format(mod))
        for error in super(Spoqa, self).check():
            yield error


class TestCase(unittest.TestCase):

    def assert_error_codes(self, expected_error_codes, filename, code):
        tree = ast.parse(code, filename or '<stdin>')
        checker = ImportOrderChecker(filename, tree)
        checker.lines = code.splitlines(True)
        checker.options = {
            'application_import_names': ['spoqa', 'tests'],
            'import_order_style': lookup_entry_point('spoqa'),
        }
        actual_error_codes = frozenset(error.code
                                       for error in checker.check_order())
        self.assertEquals(frozenset(expected_error_codes), actual_error_codes)

    def test_itself(self):
        with open(__file__) as f:
            code = f.read()
        self.assert_error_codes([], __file__, code)

    def make_test(expected_error_codes, code):
        def test_func(self):
            self.assert_error_codes(expected_error_codes,
                                    None,
                                    textwrap.dedent(code))
        return test_func

    test_valid_1 = make_test([], '''
        import datetime
        import sys
        from typing import Optional

        from pkg_resources import (SOURCE_DIST, EntryPoint, Requirement,
                                   get_provider)

        from ...deepest import a
        from ..deeper import b
        from .a import this, that
        from .z import This, That
        from spoqa import something
    ''')

    test_constants_must_be_former_than_classes = make_test(['I101'], '''
        from pkg_resources import EntryPoint, SOURCE_DIST
    ''')

    test_classes__must_be_former_than_normal_names = make_test(['I101'], '''
        from pkg_resources import get_provider, Requirement
    ''')

    test_deeper_relative_imports_must_be_latter = make_test(['I100'], '''
        from ..deeper import b
        from ...deepest import a
    ''')

    test_relative_imports_must_be_former_than_app_imports = \
        make_test(['I100'], '''
            from spoqa import b
            from .rel import a
        ''')

    test_standard_libraries_must_not_be_from_import = make_test(['I901'], '''
        from sys import argv
    ''')

    test_typing_is_only_exception_able_to_be_from_import = make_test([], '''
        import typing
        from typing import Sequence
    ''')

    test_import_typing_must_be_former_than_from_typing = make_test(
        ['I100'],
        '''
        from typing import Sequence
        import typing
        '''
    )

    test_3rd_parties_must_be_from_import = make_test(['I902'], '''
        import pkg_resources
    ''')

    test_apps_must_be_from_import = make_test(['I902'], '''
        import spoqa
    ''')
