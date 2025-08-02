from unittest import TestCase

from test_tidi import conditions_composition
from tidi import scan, get_resolver, destroy_all


class TestConditions(TestCase):
    def setUp(self) -> None:
        scan(conditions_composition)
        self.resolver = get_resolver()

    def tearDown(self) -> None:
        destroy_all()

    def test_age(self):
        result = self.resolver(int)

        self.assertEqual(result, 10)

    def test_name(self):
        result = self.resolver(str, environment='test')

        self.assertEqual(result, 'TestTimber')

    def test_multiple_candidates(self):
        result = self.resolver(str, environment='prod')

        self.assertEqual(result, 'Timber')

    def test_multiple(self):
        with self.assertRaises(Exception):
            self.resolver(str, environment='prod', anonymous='true')

    def test_setting(self):
        result = self.resolver(float, environment='prod')

        self.assertEqual(9.9, result)
