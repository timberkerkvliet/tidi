from dataclasses import dataclass

from tidi import composer, Resolver, auto_compose


@dataclass
class Point:
    x: int
    y: int


@composer
def point() -> Point:
    return Point(x=1, y=2)


@dataclass
class PointWrapper:
    point: Point


class PointWrapperWrapper:
    def __init__(self, point_wrapper: PointWrapper):
        self.point_wrapper = point_wrapper


auto_compose(PointWrapper)
auto_compose(PointWrapperWrapper)
