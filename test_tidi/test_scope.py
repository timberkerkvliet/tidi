from unittest import TestCase
from test_tidi import composition_root
from test_tidi.composition_root.scopes import Animal
from test_tidi.composition_root.some import Buzz

from tidi import scan, get_resolver


class TestResolver(TestCase):
    def setUp(self) -> None:
        scan(composition_root)
        self.resolver = get_resolver()

    def test_no_singleton(self):
        with self.assertRaises(Exception):
            self.resolver(Animal)
