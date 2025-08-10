import inspect
from typing import Type

from .resolver import Resolver


class AutoFactory:
    def __init__(self, dependency_type: Type):
        self._dependency_type = dependency_type

    def __eq__(self, other) -> bool:
        return self._dependency_type == other._dependency_type

    def __call__(self, resolver: Resolver):
        try:
            sig = inspect.signature(self._dependency_type)
        except ValueError:
            return self._dependency_type()

        params = list(sig.parameters.values())

        args = []
        for param in params:
            if param.annotation is inspect.Parameter.empty:
                raise TypeError(f"Cannot resolve untyped parameter: {param.name}")
            dependency = resolver(param.annotation)
            args.append(dependency)

        return self._dependency_type(*args)
