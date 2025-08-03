from __future__ import annotations

import typing
from typing import TypeVar, Type, Callable, Any

T = TypeVar('T')


class Resolver:
    def __init__(self, method: Callable[[Type, dict[str, str]], Any]):
        self._method = method

    @typing.overload
    def __call__(self, dependency_type: Type[T], dependency_id: str) -> T:
        """Find dependency by its ID"""

    @typing.overload
    def __call__(self, dependency_type: Type[T], **kwargs) -> T:
        """Find dependency by conditions"""

    def __call__(self, dependency_type: Type[T], **kwargs) -> T:
        return self._method(dependency_type, kwargs)

