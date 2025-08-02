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
            ScopeManager.ROOT_SCOPE_ID: Scope(parent=None, scope_type=Singleton())
        }
        self._initialized = True

    def add_composers(self, composers: list[Composer]) -> None:
        self._composers = self._composers + composers
        for scope in self._scopes.values():
            scope.add_composers(composers)

    def get_resolver(self, scope_id: str = ROOT_SCOPE_ID) -> Resolver:
        return self._scopes[scope_id].resolver()

    def create_scope(self, scope_id: str, scope_type: CustomScope, parent_id: str = ROOT_SCOPE_ID):
        scope = Scope(parent=self._scopes[parent_id], scope_type=scope_type)
        scope.add_composers(self._composers)

        self._scopes[scope_id] = scope

    def destroy_scope(self, scope_id: str):
        if scope_id == ScopeManager.ROOT_SCOPE_ID:
            raise ValueError('Root scope cannot be destroyed')

        del self._scopes[scope_id]
