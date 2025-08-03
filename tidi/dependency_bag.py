from __future__ import annotations

from typing import Any, Optional, TypeVar, Generic, Type

from .dependency import Dependency

T = TypeVar('T', bound=Dependency)


class DependencyBag:
    def __init__(self, dependencies: dict[str, Dependency]):
        self._dependencies = dependencies

    @staticmethod
    def empty() -> DependencyBag:
        return DependencyBag({})

    def add(self, dependency: Dependency) -> DependencyBag:
        return DependencyBag(
            {
                **self._dependencies,
                dependency.get_id(): dependency
            }
        )

    def find(self, dependency_type: Type, value_map: dict[str, str]) -> Optional[Dependency]:
        candidates = [
            conditional_value
            for conditional_value in self._dependencies.values()
            if issubclass(conditional_value.get_dependency_type(), dependency_type)
            and conditional_value.get_conditions().is_fulfilled_by(value_map)
        ]
        if len(candidates) == 1:
            return next(iter(candidates))
        if len(candidates) > 1:
            raise Exception(f'More than 1 candidate for type {dependency_type}')

        return None
