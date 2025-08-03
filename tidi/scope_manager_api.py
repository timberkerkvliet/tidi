from typing import Optional

from .resolver import Resolver
from .scope_manager import ScopeManager
from .scopetype import parse_scope_type


def ensure_scope(scope_id: str = 'root', scope_type: str = 'root', parent_id: Optional[str] = None) -> None:
    if parent_id is None and scope_id != 'root':
        parent_id = 'root'
    return ScopeManager().ensure_scope(scope_id, parse_scope_type(scope_type), parent_id)


def get_resolver(scope_id: str = 'root') -> Resolver:
    return ScopeManager().get_resolver(scope_id)


def clear_scope(scope_id: str) -> None:
    ScopeManager().clear_scope(scope_id=scope_id)


def clear_all_scopes() -> None:
    ScopeManager().clear_all_scopes()
