## TiDI

TiDI stands for Timber Dependency Injection. It reflects my personal approach to dependency injection, shaped by my own preferences and insights as its creator.

### True dependency injection

The essence of dependency injection is to invert the direction of dependency: the client specifies what type of dependencies it requires, while someone else decides which concrete instances to provide. Many DI frameworks blur this distinction by introducing configuration logic directly into the client—who should only declare its dependencies, not manage them. While this can seem convenient, it undermines the core value of dependency injection.

TiDI maintains this separation strictly. Consider the following client:
```
class MyClient:
    def __init__(self, dependency: MyDependency):
        ... 
```
No TiDI-specific elements are required in MyClient. Instead, composition is handled externally in a dedicated composer function:
```
@composer
def my_client() -> MyClient:
    return MyClient(MyDependency())
```
This keeps the client clean and focused and ensures that wiring and instantiation remain a separate responsibility of the composition root.

Keeping dependency composition explicitly separate is the core principle of DI—but it does come with the trade-off of writing a bit more code. TiDI aims to make defining the composition root as convenient as possible. One key feature that helps with this is _auto composition_:
```
auto_compose(MyClient)
```
This allows TiDI to automatically resolve and compose the dependencies in many cases, reducing boilerplate while preserving separation of concerns.

### Resolving dependencies

A common scenario in dependency injection is when a client depends on an interface that has multiple implementations. In such cases, the composition logic must decide which concrete implementation to provide.
```
class Repository(ABC):
    @abstractmethod
    get_by_id(id: str):
        ...

class InMemoryRepository(Repository):
    ...
    

class PostgresRepository(Repository):
    ...
```

If both `InMemoryRepository` and `PostgresRepository` have their own composers, then the type Repository becomes ambiguous—TiDI won’t know which one to resolve by default.

#### Using an identifier

The most direct way to specify which implementation to use is by assigning an explicit ID:
```
@composer(id='in-memory')
def in_memory_repository() -> InMemoryRepository:
    return InMemoryRepository()
```
You can then resolve it like this:
```
resolve(Repository, id='in-memory')
```
Since IDs are unique, this guarantees an unambiguous resolution.

#### Using filters

Alternatively, you can use _filters_ — key-value tags that don't need to be unique. This is useful for expressing environment- or context-specific choices.
```
@composer(stage='prod')
def postgres_repository() -> PostgresRepository:
    return PostgresRepository()

@composer(stage='test')
def in_memory_repository() -> InMemoryRepository:
    return InMemoryRepository()
```
Now you can resolve based on the desired context:

```
resolve(Repository, stage='test')
```
This approach offers more flexibility than IDs, allowing multiple components to share the same tags while still enabling targeted resolution.