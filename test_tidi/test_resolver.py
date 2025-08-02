from unittest import TestCase
from test_tidi import resolver_composition
from test_tidi.resolver_composition import Buzz

from tidi import scan, get_scope, clear_all_scopes


class TestResolver(TestCase):
    def setUp(self) -> None:
        scan(resolver_composition)
        self.resolver = get_scope()

    def tearDown(self) -> None:
        clear_all_scopes()

    def test_buzz(self):
        result = self.resolver(Buzz, environment='prod')

        self.assertEqual(result, Buzz('My name: Timber'))

    def test_same_instance(self):
        result_1 = self.resolver(Buzz, environment='prod')
        result_2 = self.resolver(Buzz, environment='prod')

        self.assertEqual(id(result_1), id(result_2))
