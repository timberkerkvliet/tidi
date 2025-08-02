from __future__ import annotations

from typing import Type, TypeVar, Optional

from .conditional_values import ConditionalDependencies
from .dependency import ConcreteDependency
from .composer import Composer
from .resolver import Resolver
from .scopetype import ScopeType, Singleton

T = TypeVar('T')


class Scope:
    def __init__(
        self,
        scope_id: str,
        scope_type: ScopeType,
        parent: Optional[Scope] = None
    ):
        self._scope_id = scope_id
        self._parent = parent
        self._scope_type = scope_type
        self._composers: ConditionalDependencies[Composer] = ConditionalDependencies.empty()
        self._stored_dependencies: ConditionalDependencies[ConcreteDependency] = ConditionalDependencies.empty()

    def get_id(self) -> str:
        return self._scope_id

    def get_parent(self) -> Scope:
        return self._parent

    def get_type(self) -> ScopeType:
        return self._scope_type

    @staticmethod
    def root_scope() -> Scope:
        return Scope(scope_id='root', scope_type=Singleton())

    def add_composers(self, composers: list[Composer]) -> None:
        for composer in composers:
            if composer.scope_type != self._scope_type:
                continue

            self._composers = self._composers.add(composer)

    def create(self, dependency_type: Type[T], value_map: dict[str, str]) -> T:
        composer = self._composers.find(dependency_type, value_map)
        if composer is None and self._parent is None:
            raise Exception('No composer found')
        if composer is None:
            return self._parent.create(dependency_type, value_map)

        dependency = composer.create(self.resolver(value_map))
        if composer.scope_type.supports_storing():
            self._stored_dependencies = self._stored_dependencies.add(dependency)

        return dependency.value

    def resolver(self, base_map: dict[str, str] = None) -> Resolver:
        base_map = base_map or {}
        return Resolver(lambda dep_typ, value_map: self.get(dep_typ, {**base_map, **value_map}))

    def get(self, dependency_type: Type[T], value_map: dict[str, str]) -> T:
        result = self.find(dependency_type, value_map)
        if result is not None:
            return result

        return self.create(dependency_type, value_map)

    def find(self, dependency_type: Type[T], value_map: dict[str, str]) -> Optional[T]:
        result = self._stored_dependencies.find(dependency_type, value_map)
        if result is not None:
            return result.value

        if self._parent is None:
            return None

        return self._parent.find(dependency_type, value_map)
