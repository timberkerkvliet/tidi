import importlib
import inspect
from pathlib import Path

from .composer import Composer
from .composer_repository import ComposerRepository


def walk_modules(path, prefix):
    for item in path.iterdir():
        if item.is_dir():
            yield from walk_modules(item, f"{prefix}.{item.name}")
        elif item.suffix == '.py' and item.name != '__init__.py':
            modname = f"{prefix}.{item.stem}"
            try:
                mod = importlib.import_module(modname)
                yield mod
            except Exception:
                continue


def scan(package):
    package_path = Path(package.__file__).parent
    package_name = package.__name__

    module = importlib.import_module(package_name)
    modules = [module]
    modules += list(walk_modules(package_path, package_name))

    for module in modules:
        for name, obj in inspect.getmembers(module):
            if isinstance(obj, Composer):
                ComposerRepository.add_composer(obj)
