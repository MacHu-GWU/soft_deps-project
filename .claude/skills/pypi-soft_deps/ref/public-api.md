# soft_deps public API (v0.2.0)

One public symbol: `soft_deps.api.MissingDependency`. Requires Python 3.11+.

## `MissingDependency`

```python
class MissingDependency:
    def __init__(self, name: str, error_message: str = "please install it") -> None: ...
```

Placeholder bound to the name of an optional dependency that failed to import.

| Parameter | Meaning |
| :--- | :--- |
| `name` | Name shown in the error, normally the import name (`"pandas"`). Attribute lookups extend it: `pd.DataFrame` reports `pandas.DataFrame`. |
| `error_message` | Installation hint appended to the error, such as `"pip install your_library[excel]"`. Write it without a trailing period; one is added. |

Error text: ``To use `<name>`, <error_message>.``

### Usage

```python
from soft_deps.api import MissingDependency

try:
    import pandas as pd
except ImportError:
    pd = MissingDependency("pandas", "pip install pandas")


def export_to_excel(data: dict) -> pd.DataFrame:
    return pd.DataFrame(data)


try:
    export_to_excel({"a": [1]})
except ImportError as e:
    print(e)  # To use `pandas.DataFrame`, pip install pandas.
```

To keep IDE autocomplete on a name whose module may be missing even on the developer machine, import it under `typing.TYPE_CHECKING` inside the `try`:

```python
import typing as T

try:
    if T.TYPE_CHECKING:
        from your_library import important_library
    raise ImportError
except ImportError:
    important_library = MissingDependency("important_library")
```

### Behavior

Mentioning the placeholder returns another placeholder; using it raises `ImportError`.

| Operation | Result |
| :--- | :--- |
| `pd.attr` (public name) | `MissingDependency("pandas.attr")` |
| `pd[...]` | `MissingDependency("pandas[...]")`, for generic hints such as `npt.NDArray[np.float64]` |
| `pd.X \| None`, `None \| pd.X` | a placeholder, for `X \| None` hints |
| `pd._x`, `pd.__x__` | `AttributeError`, so `hasattr()` returns `False` and `copy`, `pickle`, `inspect.unwrap`, `pydoc`, doctest collection work |
| `repr(pd)` | `"MissingDependency('pandas')"` |
| `pd == x`, `hash(pd)`, `pd in [...]`, `{pd}` | identity semantics, like a plain object |
| `bool(pd)` | `True`, like a real module |
| `pd(...)`, `str(pd)`, `f"{pd}"`, `iter(pd)`, `len(pd)`, `with pd:` | `ImportError` |
| `<`, `<=`, `>`, `>=`, `+`, `-`, `*`, `/` | `ImportError` |
| `isinstance(x, pd.X)`, `issubclass(C, pd.X)`, `class C(pd.X)` | `ImportError` |

### Gotchas

- Type hints never raise, on any supported Python, with or without `from __future__ import annotations`, and also when evaluated by `typing.get_type_hints()` (pydantic, typer, Sphinx).
- Code that runs at import time and *uses* the dependency still fails the import: decorators (`@numba.jit`), subclasses (`class M(pydantic.BaseModel)`), module-level calls. Move it into a module that only the optional feature imports.
- `except pd.SomeError:` raises `TypeError` when an exception reaches it, because the placeholder is not an exception class.
- The placeholder has no public attributes of its own; `pd.name` is a placeholder for `pandas.name`.
