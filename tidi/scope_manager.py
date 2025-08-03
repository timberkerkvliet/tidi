from typing import Optional

from .composer import Composer
from .scope import Scope
from .scopetype import ScopeType, RootType
from .resolver import Resolver


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
        self._scopes: dict[str, Scope] = {}
        self._initialized = True

    def add_composers(self, composers: list[Composer]) -> None:
        self._composers = self._composers + composers
        for scope in self._scopes.values():
            scope.add_composers(composers)

    def ensure_scope(self, scope_id: str, scope_type: ScopeType, parent_id: Optional[str] = None) -> None:
        if scope_id not in self._scopes:
            self.create_scope(scope_id, scope_type, parent_id)
            return

        existing_scope = self._scopes[scope_id]
        if existing_scope.get_type() != scope_type:
            raise Exception
        if existing_scope.get_parent() is None and parent_id is not None:
            raise Exception
        if existing_scope.get_parent() is not None and existing_scope.get_parent().get_id() != parent_id:
            raise Exception

    def get_resolver(self, scope_id: str) -> Resolver:
        self.ensure_scope(scope_id='root', scope_type=RootType())
        return self._scopes[scope_id].resolver()

    def create_scope(self, scope_id: str, scope_type: ScopeType, parent_id: str = ROOT_SCOPE_ID) -> None:
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
