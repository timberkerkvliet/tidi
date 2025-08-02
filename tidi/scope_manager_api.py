from .scope_manager import ScopeManager
from .resolver import Resolver


def get_resolver(scope_id: str = 'root') -> Resolver:
    return ScopeManager().get_resolver(scope_id)


def create_scope(scope_id: str = 'root') -> Resolver:
    return ScopeManager().create_scope(scope_id)