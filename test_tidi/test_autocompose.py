from unittest import TestCase

from test_tidi import composition_root
from test_tidi.composition_root.autocompose import PointWrapper, Point
from tidi import scan, get_resolver, destroy_all


class TestAutoCompose(TestCase):
    def setUp(self) -> None:
        scan(composition_root)
        scan(composition_root)
        self.resolver = get_resolver()

    def tearDown(self) -> None:
        destroy_all()

    def test_no_singleton(self):
        result = self.resolver(PointWrapper)

        self.assertEqual(PointWrapper(point=Point(x=1, y=2)), result)
