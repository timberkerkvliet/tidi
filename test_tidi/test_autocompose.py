from unittest import TestCase

from test_tidi import autocompose_composition
from test_tidi.autocompose_composition import PointWrapper, Point
from tidi import scan, get_resolver, destroy_all


class TestAutoCompose(TestCase):
    def setUp(self) -> None:
        scan(autocompose_composition)
        scan(autocompose_composition)
        self.resolver = get_resolver()

    def tearDown(self) -> None:
        destroy_all()

    def test_no_singleton(self):
        result = self.resolver(PointWrapper)

        self.assertEqual(PointWrapper(point=Point(x=1, y=2)), result)
