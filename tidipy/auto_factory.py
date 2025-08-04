import inspect
from typing import Type

from .resolver import Resolver


class AutoFactory:
    def __init__(self, dependency_type: Type):
        self._dependency_type = dependency_type

    def __eq__(self, other) -> bool:
        if not isinstance(other, AutoFactory):
            return False

        return self._dependency_type == other._dependency_type

    def __call__(self, resolver: Resolver):
        constructor = self._dependency_type.__init__
        sig = inspect.signature(constructor)

        params = list(sig.parameters.values())[1:]

        args = []
        for param in params:
            if param.annotation is inspect.Parameter.empty:
                raise TypeError(f"Cannot resolve untyped parameter: {param.name}")
            dependency = resolver(param.annotation)
            args.append(dependency)

        return self._dependency_type(*args)
