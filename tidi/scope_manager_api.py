from typing import Optional

from .resolver import Resolver
from .scope_manager import ScopeManager
from .scopetype import parse_scope_type


def get_scope(scope_id: str = 'root', scope_type: str = 'root', parent_id: Optional[str] = None) -> Resolver:
    if parent_id is None and scope_id != 'root':
        parent_id = 'root'
    return ScopeManager().get_scope(scope_id, parse_scope_type(scope_type), parent_id).resolver()


def clear_scope(scope_id: str) -> None:
    ScopeManager().clear_scope(scope_id=scope_id)


def clear_all_scopes() -> None:
    ScopeManager().clear_all_scopes()
