from abc import ABC, abstractmethod

from tidi import auto_compose, composer


class StringGenerator(ABC):
    @abstractmethod
    def generate(self) -> str:
        pass


class TimberGenerator(StringGenerator):
    def generate(self) -> str:
        return 'Timber'


class HelloGenerator(StringGenerator):
    def generate(self) -> str:
        return 'Hello'


@composer(environment='prod')
def timber() -> TimberGenerator:
    return TimberGenerator()


@composer(environment='test')
def hello() -> HelloGenerator:
    return HelloGenerator()
