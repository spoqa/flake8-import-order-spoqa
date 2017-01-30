import unittest

from flake8_import_order.styles import Style

__all__ = 'Spoqa',


class Spoqa(Style):

    @staticmethod
    def name_key(identifier):
        name = identifier.lstrip('_')
        hidden = name != identifier
        if name.isupper():
            return 0, hidden  # constants e.g. CONSTANT_NAME
        elif name[0].isupper():
            return 1, hidden  # classes e.g. ClassName
        else:
            return 2, hidden  # normal variables e.g. normal_names

    @classmethod
    def sorted_names(cls, names):
        return sorted(names, key=cls.name_key)

    @classmethod
    def import_key(cls, import_):
        modules = [cls.name_key(module) for module in import_.modules]
        names = [cls.name_key(name) for name in import_.names]
        return (import_.type, import_.level, modules, names)


class TestCase(unittest.TestCase):
    def test_sample(self):
        self.assertEquals(1, 2)
