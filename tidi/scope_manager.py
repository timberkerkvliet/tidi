from typing import Optional

from .conditional_values import ConditionalDependencies
from .composer import Composer
from .scopetype import Singleton, CustomScope
from .resolver import Resolver
from .scope import Scope


class ScopeManager:
    ROOT_SCOPE_ID = 'root'
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._composers = []
        self._scopes: dict[str, Scope] = {
            'root': Scope.root_scope()
        }
        self._initialized = True

    def add_composers(self, composers: list[Composer]) -> None:
        self._composers = self._composers + composers
        for scope in self._scopes.values():
            scope.add_composers(composers)

    def get_resolver(self, scope_id: str, scope_type: CustomScope, parent_id: Optional[str] = None) -> Resolver:
        if scope_id not in self._scopes:
            self.create_scope(scope_id, scope_type, parent_id)
            return self._scopes[scope_id].resolver()

        existing_scope = self._scopes[scope_id]
        if existing_scope.get_type() != scope_type:
            raise Exception

        return self._scopes[scope_id].resolver()

    def create_scope(self, scope_id: str, scope_type: CustomScope, parent_id: str = ROOT_SCOPE_ID) -> None:
        scope = Scope(
            scope_id=scope_id,
            parent=self._scopes[parent_id] if parent_id is not None else None,
            scope_type=scope_type
        )
        scope.add_composers(self._composers)

        if scope_id in self._scopes:
            raise Exception('Scope already exists')

        self._scopes[scope_id] = scope

    def clear_scope(self, scope_id: str):
        del self._scopes[scope_id]

    def clear_all_scopes(self) -> None:
        self._scopes: dict[str, Scope] = {}
