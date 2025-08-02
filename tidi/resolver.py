from __future__ import annotations

from typing import TypeVar, Type, Callable, Any

T = TypeVar('T')


class Resolver:
    def __init__(self, method: Callable[[Type, dict[str, str]], Any]):
        self._method = method

    def __call__(self, dependency_type: Type[T], **kwargs) -> T:
        return self._method(dependency_type, kwargs)
