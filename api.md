## API reference

Everything can be imported from the root of the package:

```
from tidypy import composer, auto_compose, ensure_scope, clear_scope, reset, add_context, get_resolver, scan
```

### composer

`composer` is a function decorator that takes as arguments:
* `id: str`: the id of this dependency
* `scope_type: str`: the types of scopes in which it is available
* `kwargs: str | set[str]`: the values in the scope context for which this dependency is available

### auto_compose

`auto_compose` is a function that takes a class as its first arguments and will auto compose based on the typing in its `__init__`. Apart from this argument, it has the same arguments as `composer`.

### ensure_scope

`ensure_scope` is a function checks that a scope with the given properties already exists and if not creates one. It takes as arguments:
* `scope_id: str` the target scope
* `scope_type: str` the type this scope should have
*  `parent_id` the ID of the parent scope

### clear_scope

`clear_scope` is a function that clears a scope and all of its children. It has `scope_id: str` as argument.

### reset

`reset` is a function that resets TiDI completely. It clears all scopes and forgets all registered composers.

### add_context

`add_context` is a function that adds context values to a scope. It takes as arguments:
* `scope_id: str` the target scope
* `kwargs: str` the values to add

### get_resolver

`get_resolver` is a function that gets the resolver of a certain scope. It takes `scope_id: str` as argument to indicate the target scope.

### scan

`scan` is a function that scans a python module for composers. It takes a module as an argument:

```
from my_project import composition_root

scan(composition_root)
```
