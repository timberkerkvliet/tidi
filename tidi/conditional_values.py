from __future__ import annotations

from typing import Any, Optional, TypeVar, Generic, Type

from .dependency import Dependency

T = TypeVar('T', bound=Dependency)


class ConditionalDependencies(Generic[T]):
    def __init__(self, values: list[T]):
        self._values: dict[str, T] = {
            value.get_id(): value
            for value in values
        }

    @staticmethod
    def empty() -> ConditionalDependencies:
        return ConditionalDependencies([])

    def add(self, conditional_value: T) -> ConditionalDependencies[T]:
        return ConditionalDependencies(
            list(self._values.values()) + [conditional_value]
        )

    def find(self, dependency_type: Type, value_map: dict[str, str]) -> Optional[T]:
        candidates = [
            conditional_value
            for conditional_value in self._values.values()
            if issubclass(dependency_type, conditional_value.get_dependency_type())
            and conditional_value.get_conditions().is_fulfilled_by(value_map)
        ]
        if len(candidates) == 1:
            return next(iter(candidates))
        if len(candidates) > 1:
            raise Exception('More than 1 candidate')

        return None
