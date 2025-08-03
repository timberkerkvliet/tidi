from unittest import TestCase

from test_tidi import context_composition
from test_tidi.context_composition import StringGenerator, HelloGenerator, TimberGenerator
from tidi import scan, get_resolver, reset, add_context


class TestContext(TestCase):
    def setUp(self) -> None:
        scan(context_composition)
        self.resolver = get_resolver()

    def tearDown(self) -> None:
        reset()

    def test_production(self):
        add_context(environment='prod')
        result = self.resolver(StringGenerator)

        self.assertEqual(result.generate(), 'Timber')

    def test_specific_type(self):
        add_context(environment='test')
        result = self.resolver(HelloGenerator)

        self.assertEqual(result.generate(), 'Hello')

    def test_resolves_with_additional_values(self):
        add_context(environment='test', some_extra_key='iets')
        result = self.resolver(HelloGenerator)

        self.assertEqual(result.generate(), 'Hello')

    def test_cannot_resolve_with_multiple_candidates(self):
        with self.assertRaises(Exception):
            self.resolver(StringGenerator)

    def test_can_resolve_specific(self):
        result = self.resolver(TimberGenerator)

        self.assertEqual(result.generate(), 'Timber')
