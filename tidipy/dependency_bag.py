from __future__ import annotations

from typing import Optional, Type, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .resolver import Resolver
    from .dependency import Dependency, Composer


class DependencyBag:
    def __init__(self, composers: list[Composer]):
        self._composers = composers
        self._dependencies: dict[str, Any] = {}

    def _get_candidates(
        self,
        dependency_type: Type,
        dependency_id: Optional[str]
    ) -> list[Composer]:
        candidates = [
            dependency
            for dependency in self._composers
            if issubclass(dependency.get_dependency_type(), dependency_type)
        ]
        if dependency_id is not None:
            candidates = [dependency for dependency in candidates if dependency.get_id() == dependency_id]

        return candidates

    def find(
        self,
        dependency_type: Type,
        dependency_id: Optional[str],
        resolver: Resolver
    ) -> Optional[Dependency]:
        candidates = self._get_candidates(dependency_type, dependency_id)

        if len(candidates) == 0:
            return None
        if len(candidates) > 1:
            raise Exception(f'More than 1 candidate for type {dependency_type}')

        composer = next(iter(candidates))
        composer_id = composer.get_id()
        if composer_id in self._dependencies:
            return self._dependencies[composer_id]

        dependency = composer.factory(resolver)

        if composer.supports_storing():
            self._dependencies[composer_id] = dependency

        return dependency
