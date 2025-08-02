import importlib
import inspect
import pkgutil

from .composer import Composer
from .scope_manager import ScopeManager


def scan(package):
    composers = []

    def walk_modules(pkg):
        for _, modname, ispkg in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + '.'):
            try:
                mod = importlib.import_module(modname)
                yield mod
                if ispkg and hasattr(mod, '__path__'):
                    yield from walk_modules(mod)
            except Exception as e:
                print(f"Error importing {modname}: {e}")

    for mod in [package] + list(walk_modules(package)):
        for name, obj in inspect.getmembers(mod):
            if isinstance(obj, Composer):
                composers.append(obj)

    ScopeManager().add_composers(composers)
