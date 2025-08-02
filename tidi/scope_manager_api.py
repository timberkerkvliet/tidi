from typing import Optional

from .scope_manager import ScopeManager
from .resolver import Resolver
from .scopetype import ScopeType, parse_scope_type, CustomScope


def get_resolver(scope_id: str = 'root') -> Resolver:
    return ScopeManager().get_resolver(scope_id)


def create_scope(scope_id: str, scope_type: str, parent_id: str = 'root') -> None:
    scope_type = parse_scope_type(scope_type)
    if not isinstance(scope_type, CustomScope):
        raise ValueError
    ScopeManager().create_scope(scope_id=scope_id, scope_type=scope_type, parent_id=parent_id)


def ensure_scope(scope_id: str, scope_type: str, parent_id: str = 'root') -> None:
    scope_type = parse_scope_type(scope_type)
    if not isinstance(scope_type, CustomScope):
        raise ValueError
    ScopeManager().ensure_scope(scope_id=scope_id, scope_type=scope_type, parent_id=parent_id)
