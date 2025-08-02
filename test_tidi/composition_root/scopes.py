from dataclasses import dataclass

from tidi import composer, Resolver


@dataclass
class Hey:
    age: int


@dataclass
class Animal:
    name: str


@composer
def hey() -> Hey:
    return Hey(17)


@composer(scope='tenant')
def animal() -> Animal:
    return Animal(name='Henk')
