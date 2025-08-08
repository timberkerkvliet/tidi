from __future__ import annotations

from typing import TypeVar, Optional

from .dependency import Composer
from .dependency_bag import DependencyBag
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

        self._context = context if parent is None else context.add(parent.get_context().values())

        self._resolver = Resolver(
            context=self._context,
            parent=self._parent.resolver() if self._parent is not None else None,
            dependency_bag=DependencyBag.from_dependencies({
                composer
                for composer in composers
                if not composer.scope_type.supports_storing() or composer.scope_type == scope_type
            })
        )
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

    def add_scope(
        self,
        scope_id: str,
        scope_type: ScopeType,
        context: ScopeContext
    ):
        self._children[scope_id] = Scope(
            scope_id=scope_id,
            parent=self,
            scope_type=scope_type,
            composers=self._composers,
            context=context
        )

    def find_scope(self, scope_id: str) -> Optional[Scope]:
        if scope_id == self._scope_id:
            return self

        for child_id, child in self._children.items():
            result = child.find_scope(scope_id)
            if result is not None:
                return result

        return None

    def remove_scope(self, scope_id: str) -> None:
        if scope_id in self._children:
            self._children.pop(scope_id)

        for child_id, child in self._children.items():
            child.remove_scope(scope_id)

    def get_id(self) -> str:
        return self._scope_id

    def get_parent(self) -> Scope:
        return self._parent

    def get_type(self) -> ScopeType:
        return self._scope_type

    def get_ancestors(self) -> set[Scope]:
        if self._parent is None:
            return set()

        return {self._parent} | self._parent.get_ancestors()

    def get_ancestor_types(self) -> set[ScopeType]:
        return {scope.get_type() for scope in self.get_ancestors()}

    def get_context(self) -> ScopeContext:
        return self._context

    def resolver(self) -> Resolver:
        return self._resolver
