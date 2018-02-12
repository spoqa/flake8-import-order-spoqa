import ast
import textwrap
import unittest

from flake8_import_order import ImportType
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
            return 2, hidden, name
        elif name.isupper():
            return 0, hidden, name  # constants e.g. CONSTANT_NAME
        elif name[0].isupper():
            return 1, hidden, name  # classes e.g. ClassName
        else:
            return 2, hidden, name  # normal variables e.g. normal_names

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
        group_value = group.value
        if group in (ImportType.APPLICATION, ImportType.APPLICATION_PACKAGE):
            group_value += ImportType.APPLICATION_RELATIVE.value
        return group_value, -import_.level, modules, names

    def _check(self, previous_import, previous, current_import):
        bases = super(Spoqa, self)._check(
            previous_import,
            previous,
            current_import
        )
        for error in bases:
            yield error
        mod = current_import.modules[0]
        type_ = current_import.type
        is_from = current_import.is_from
        lineno = current_import.lineno
        if type_ == ImportType.STDLIB and is_from and \
           mod not in self.from_importable_standard_librarires:
            yield Error(lineno, 'I901',
                        'A standard library is imported using '
                        '"from {0} import ..." statement. Should be '
                        '"import {0}" instead.'.format(mod))
        elif type_ == ImportType.THIRD_PARTY and not is_from:
            yield Error(lineno, 'I902',
                        'A third party library is imported using '
                        '"import {0}" statement. Should be '
                        '"from {0} import ..." instead.'.format(mod))
        elif type_ in (ImportType.APPLICATION,
                       ImportType.APPLICATION_PACKAGE) and not is_from:
            yield Error(lineno, 'I902',
                        'An app module is imported using "import {0}"'
                        ' statement. Should be "from {0} import ..."'
                        ' instead.'.format(mod))


class TestCase(unittest.TestCase):

    def assert_error_codes(self, expected_error_codes, filename, code):
        try:
            tree = ast.parse(code, filename or '<stdin>')
        except TypeError as e:
            raise TypeError(
                '{0!s}\ncode = {1!r}\nfilename = {2!r}'.format(
                    e, code, filename
                )
            )
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
        from .a import that, this
        from .z import That, This
        from spoqa import something
    ''')

    test_valid_2 = make_test([], '''
        from typing import List, Optional

        from spoqa import CONSTANT_NAME, TypeName, func_name, var_name
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

    test_names_must_be_ordered_lexicographically = make_test(['I101'], '''
        from spoqa import b, a
    ''')

    test_names_must_be_sorted = make_test(['I101'], '''
        from spoqa import a, B, c
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
