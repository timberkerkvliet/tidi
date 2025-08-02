from abc import ABC, abstractmethod
from dataclasses import dataclass


class ScopeType(ABC):
    @abstractmethod
    def supports_storing(self) -> bool:
        pass


@dataclass
class Singleton(ScopeType):
    def supports_storing(self) -> bool:
        return True


@dataclass
class Transient(ScopeType):
    def supports_storing(self) -> bool:
        return False


@dataclass
class CustomScope(ScopeType):
    scope_type: str

    def supports_storing(self) -> bool:
        return True


def parse_scope_type(value: str) -> ScopeType:
    if value == 'singleton':
        return Singleton()
    if value == 'transient':
        return Transient()

    return CustomScope(value)
