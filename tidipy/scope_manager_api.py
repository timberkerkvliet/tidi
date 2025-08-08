from typing import Optional

from .resolver import Resolver
from .scope import Scope
from .scope_context import ScopeContext
from .composer_repository import ComposerRepository
from .scope_type import parse_scope_type, RootType


class RootScopeProvider:
    _root_scope: Optional[Scope] = None

    @classmethod
    def get(cls) -> Scope:
        if cls._root_scope is None:
            RootScopeProvider._root_scope = Scope(
                scope_id='root',
                scope_type=RootType(),
                composers=ComposerRepository.get_composers(),
                context=ScopeContext.empty()
            )

        return cls._root_scope

    @classmethod
    def reset(cls) -> None:
        cls._root_scope = None

def ensure_scope(
    scope_id: str,
    scope_type: str,
    parent_id: str = 'root',
    context: Optional[dict[str, str]] = None
) -> None:
    parsed_scope_type=parse_scope_type(scope_type)
    parsed_context=ScopeContext(context) if context is not None else ScopeContext.empty()

    existing_scope = RootScopeProvider.get().find_scope(scope_id)

    if existing_scope is None:
        RootScopeProvider.get().find_scope(parent_id).add_scope(
            scope_id=scope_id,
            scope_type=parsed_scope_type,
            context=parsed_context
        )
        return


    if existing_scope.get_type() != parsed_scope_type:
        raise Exception
    if existing_scope.get_parent() is None and parent_id is not None:
        raise Exception
    if existing_scope.get_parent() is not None and existing_scope.get_parent().get_id() != parent_id:
        raise Exception
    if context is not None and existing_scope.get_context() != parsed_context:
        raise Exception


def get_resolver(scope_id: str = 'root') -> Resolver:
    return RootScopeProvider.get().find_scope(scope_id).resolver()


def clear_scope(scope_id: str) -> None:
    return RootScopeProvider.get().remove_scope(scope_id)


def reset() -> None:
    RootScopeProvider.reset()
    ComposerRepository.reset()
