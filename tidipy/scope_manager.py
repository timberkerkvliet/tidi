from .dependency import Composer
from .scope import Scope


class ScopeManager:
    def __init__(self):
        self._composers: set[Composer] = set()

    def add_composer(self, composer: Composer) -> None:
        if composer in self._composers:
            return
        existing_ids = {composer.id for composer in self._composers}
        if composer.id in existing_ids:
            raise Exception(f'Duplicate composer with id {composer.id}')

        self._composers.add(composer)

    def get_composers(self) -> set[Composer]:
        return self._composers

    def reset(self) -> None:
        self.__init__()


scope_manager = ScopeManager()
