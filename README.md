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

A typical example is when a client depends on an interface that have multiple implementations. In that case, when creating the client it needs to be specified which concrete instance to use.

```
class Repository(ABC):
    @abstractmethod
    get_by_id(id: str):
        ...
```

#### Using an identifier

```
@composer(id='in-memory')
def in_memory_repository() -> InMemoryRepository:
    return InMemoryRepository()
```


```
resolve(Repository, id='in-memory')
```

#### Using filters

```
@composer(stage='test')
def in_memory_repository() -> InMemoryRepository:
    return InMemoryRepository()
```


```
resolve(Repository, stage='test')
```
