from unittest import TestCase

from test_tidi import autocompose_composition
from test_tidi.autocompose_composition import PointWrapper, Point
from tidi import scan, get_scope, clear_all_scopes, auto_compose


class TestAutoCompose(TestCase):
    def setUp(self) -> None:
        scan(autocompose_composition)
        scan(autocompose_composition)
        self.resolver = get_scope()

    def tearDown(self) -> None:
        clear_all_scopes()

    def test_point_wrapper(self):
        result = self.resolver(PointWrapper)

        self.assertEqual(PointWrapper(point=Point(x=1, y=2)), result)
