from __future__ import annotations

from dataclasses import dataclass
from typing import Type, Any, Callable

from .conditions import Conditions
from .resolver import Resolver
from .scope_type import ScopeType, RootType


@dataclass(frozen=True)
class Composer:
    id: str
    scope_type: ScopeType
    conditions: Conditions
    factory: Callable[[Resolver], Any]
    dependency_type: Type

    def get_id(self) -> str:
        return self.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __post_init__(self):
        if self.scope_type == RootType() and not self.conditions.is_empty():
            raise Exception('Dependency with root scope type cannot have conditions')

    def supports_storing(self) -> bool:
        return self.scope_type.supports_storing()
