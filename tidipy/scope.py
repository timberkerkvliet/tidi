from __future__ import annotations

from typing import TypeVar, Optional

from .children import Children
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
        self._children: Children[Scope] = Children(self, {})
        self._scope_type = scope_type
        self._composers = composers
        self._context = context

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
        self._children.add_child(
            Scope(
                scope_id=scope_id,
                parent=self,
                scope_type=scope_type,
                composers=self._composers,
                context= context.add(self._context.values())
            )
        )

    def find_scope(self, scope_id: str) -> Optional[Scope]:
        return self._children.find_descendant(scope_id)

    def remove_scope(self, scope_id: str) -> None:
        self._children.remove_descendant(scope_id)

    def get_id(self) -> str:
        return self._scope_id

    def matches(self, scope_type: ScopeType, parent_id: Optional[str], context: Optional[ScopeContext]) -> bool:
        if self._scope_type != scope_type:
            return False
        if self._parent is None and parent_id is not None:
            return False
        if self._parent is not None and self._parent.get_id() != parent_id:
            return False
        if context is not None and not context.part_of(self._context):
            return False

        return True

    def get_type(self) -> ScopeType:
        return self._scope_type

    def get_ancestors(self) -> set[Scope]:
        if self._parent is None:
            return set()

        return {self._parent} | self._parent.get_ancestors()

    def get_ancestor_types(self) -> set[ScopeType]:
        return {scope.get_type() for scope in self.get_ancestors()}

    def resolver(self) -> Resolver:
        return self._resolver
