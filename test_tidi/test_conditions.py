from unittest import TestCase

from test_tidi import conditions_composition
from test_tidi.conditions_composition import StringGenerator, HelloGenerator, TimberGenerator
from tidi import scan, get_scope, clear_all_scopes


class TestConditions(TestCase):
    def setUp(self) -> None:
        scan(conditions_composition)
        self.resolver = get_scope()

    def tearDown(self) -> None:
        clear_all_scopes()

    def test_production(self):
        result = self.resolver(StringGenerator, environment='prod')

        self.assertEqual(result.generate(), 'Timber')

    def test_specific_type(self):
        result = self.resolver(HelloGenerator, environment='test')

        self.assertEqual(result.generate(), 'Hello')

    def test_resolves_with_additional_values(self):
        result = self.resolver(HelloGenerator, environment='test', some_extra_key='iets')

        self.assertEqual(result.generate(), 'Hello')

    def test_has_multiple(self):
        with self.assertRaises(Exception):
            self.resolver(StringGenerator)

    def test_can_resolve_specific(self):
        result = self.resolver(TimberGenerator)

        self.assertEqual(result.generate(), 'Timber')
