from __future__ import annotations

from typing import Type, TypeVar, Optional, Any

from .dependency_bag import DependencyBag
from .dependency import ConcreteDependency, Dependency, Composer
from .resolver import Resolver
from .scope_context import ScopeContext
from .scope_type import ScopeType, RootType, Transient

T = TypeVar('T')


class Scope:
    def __init__(
        self,
        scope_id: str,
        scope_type: ScopeType,
        composers: set[Composer],
        context: ScopeContext,
        parent: Optional[Scope] = None
    ):
        self._scope_id = scope_id
        self._parent = parent
        self._children: dict[str, Scope] = {}
        self._scope_type = scope_type
        self._composers = composers
        self._dependency_bag: DependencyBag = DependencyBag.from_dependencies({
            composer
            for composer in composers
            if not composer.scope_type.supports_storing() or composer.scope_type == scope_type
        })
        self._context = context if parent is None else context.add(parent.get_context().values())
        self._validate()

    def _validate(self):
        if self._scope_id == 'root' and self._scope_type != RootType():
            raise Exception('Only root scope can have root type')
        if self._scope_id != 'root' and self._scope_type == RootType():
            raise Exception('Only root scope can have root type')
        if self._scope_id == 'root' and self._parent is not None:
            raise Exception('Root scope can not have parent')
        if self._scope_type in self.get_ancestor_types():
            raise Exception('Ancestor already has a scope of this type')
        if self._scope_type == Transient():
            raise Exception('Scopes can not have type transient')

    def add_child(
        self,
        scope_id: str,
        scope_type: ScopeType,
        context: Optional[ScopeContext] = None
    ):
        scope = Scope(
            scope_id=scope_id,
            parent=self,
            scope_type=scope_type,
            composers=self._composers,
            context=context
        )
        self._children[scope_id] = scope

    def get_id(self) -> str:
        return self._scope_id

    def get_parent(self) -> Scope:
        return self._parent

    def get_type(self) -> ScopeType:
        return self._scope_type

    def __hash__(self) -> int:
        return hash(self._scope_id)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Scope):
            return False

        return self._scope_id == other.get_id()

    def get_ancestors(self) -> set[Scope]:
        if self._parent is None:
            return set()

        return {self._parent} | self._parent.get_ancestors()

    def get_ancestor_types(self) -> set[ScopeType]:
        return {scope.get_type() for scope in self.get_ancestors()}

    def get_context(self) -> ScopeContext:
        return self._context

    def resolver(self, context: Optional[ScopeContext] = None) -> Resolver:
        context = self._context if context is None else context
        return Resolver(lambda dependency_type, dependency_id: self._get(dependency_type, dependency_id, context))

    def _get(
        self,
        dependency_type: Type,
        dependency_id: Optional[str],
        context: Optional[ScopeContext] = None
    ) -> Any:
        context = self._context if context is None else context
        result = self._dependency_bag.find(
            dependency_type,
            dependency_id,
            self.resolver(context),
            context
        )
        if result is not None:
            return result

        if self._parent is None:
            raise Exception(f'No candidate for type {dependency_type}')

        return self._parent._get(dependency_type, dependency_id, self._context)
