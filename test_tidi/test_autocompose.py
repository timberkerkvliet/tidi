from unittest import TestCase

from test_tidi import autocompose_composition
from test_tidi.autocompose_composition import PointWrapper, Point, PointWrapperWrapper
from tidipy import scan, get_resolver, reset, auto_compose


class TestAutoCompose(TestCase):
    def setUp(self) -> None:
        scan(autocompose_composition)

        auto_compose(PointWrapper)
        auto_compose(PointWrapperWrapper)

        self.resolver = get_resolver()

    def tearDown(self) -> None:
        reset()

    def test_point_wrapper(self):
        result = self.resolver(PointWrapper)

        self.assertEqual(PointWrapper(point=Point(x=1, y=2)), result)

    def test_point_wrapper_wrapper(self):
        result = self.resolver(PointWrapperWrapper)

        self.assertEqual(PointWrapper(point=Point(x=1, y=2)), result.point_wrapper)
