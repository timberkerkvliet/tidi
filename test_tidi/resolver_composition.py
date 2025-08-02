from dataclasses import dataclass

from tidi import composer, Resolver


@composer
def my_name() -> str:
    return 'Timber'


@dataclass
class Buzz:
    description: str


@composer
def buzz(resolve: Resolver) -> Buzz:
    name = resolve(str)
    return Buzz(description=f'My name: {name}')
