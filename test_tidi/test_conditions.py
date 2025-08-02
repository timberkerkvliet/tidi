from unittest import TestCase

from test_tidi import conditions_composition
from test_tidi.conditions_composition import StringGenerator
from tidi import scan, get_resolver, destroy_all


class TestConditions(TestCase):
    def setUp(self) -> None:
        scan(conditions_composition)
        self.resolver = get_resolver()

    def tearDown(self) -> None:
        destroy_all()

    def test_production(self):
        result = self.resolver(StringGenerator, environment='prod')

        self.assertEqual(result.generate(), 'Timber')

    def test_multiple(self):
        with self.assertRaises(Exception):
            self.resolver(StringGenerator)
