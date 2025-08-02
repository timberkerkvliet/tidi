from unittest import TestCase
from test_tidi import composition_root
from test_tidi.composition_root.some import Buzz

from tidi import scan, get_resolver, destroy_all


class TestResolver(TestCase):
    def setUp(self) -> None:
        scan(composition_root)
        self.resolver = get_resolver()

    def tearDown(self) -> None:
        destroy_all()

    def test_buzz(self):
        result = self.resolver(Buzz, environment='prod')

        self.assertEqual(result, Buzz('My name: Timber'))

    def test_same_instance(self):
        result_1 = self.resolver(Buzz, environment='prod')
        result_2 = self.resolver(Buzz, environment='prod')

        self.assertEqual(id(result_1), id(result_2))
