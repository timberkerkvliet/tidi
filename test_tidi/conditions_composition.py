from dataclasses import dataclass

from tidi import composer, Resolver


@composer
def age() -> int:
    return 10


@composer(environment={'prod', 'test'})
def setting() -> float:
    return 9.9


@composer(environment='prod')
def my_name() -> str:
    return 'Timber'


@composer(environment='prod', anonymous='true')
def another_name() -> str:
    return 'Second Name'


@composer(environment='test')
def my_name_test() -> str:
    return 'TestTimber'


@dataclass
class Buzz:
    description: str


@composer(environment='prod')
def buzz(resolve: Resolver) -> Buzz:
    name = resolve(str)
    return Buzz(description=f'My name: {name}')
