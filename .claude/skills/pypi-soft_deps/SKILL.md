---
name: pypi-soft_deps
description: Python library soft_deps (v0.2.0) — import optional dependencies so a library still imports when they are missing, keeps full IDE autocomplete when they are installed, and raises a clear ImportError with an install hint only when the missing dependency is actually used. Public API: MissingDependency.
---

# soft_deps

Optional dependency handling for Python libraries (Python 3.11+). Import the dependency normally inside `try`; in `except ImportError`, bind the same name to a `MissingDependency` placeholder. With the dependency installed you get the real module and full IDE support. Without it, the library still imports, and the first real use raises `ImportError` with an installation hint.

## Import

```python
from soft_deps.api import MissingDependency
```

or

```python
import soft_deps.api as soft_deps
# then soft_deps.MissingDependency
```

## Public API

- `MissingDependency(name: str, error_message: str = "please install it")`: placeholder for a dependency that is not installed. Its error reads ``To use `<name>.<attr path>`, <error_message>.``. It has no public methods or attributes: every public attribute name belongs to the missing dependency.

## Pattern

Put all optional imports in one module, and use the names only inside functions:

```python
# your_library/importer.py
from soft_deps.api import MissingDependency

try:
    import pandas as pd
except ImportError:
    pd = MissingDependency("pandas", "pip install your_library[excel]")
```

```python
# your_library/excel.py
from .importer import pd

def export_to_excel(data: dict, path: str) -> pd.DataFrame:  # type hint is fine
    df = pd.DataFrame(data)  # raises ImportError here if pandas is missing
    df.to_excel(path)
    return df
```

## What raises

| Does not raise | Raises `ImportError` |
| :--- | :--- |
| `pd.DataFrame`, `npt.NDArray[np.float64]`, `pd.DataFrame \| None` (return another placeholder, so type hints and `typing.get_type_hints()` work with or without `from __future__ import annotations`) | calling: `pd.DataFrame(data)` |
| `repr()`, `==`, `hash()`, `in [...]`, `copy`, `pickle`, `bool()` (always `True`) | `str()`, f-strings, iteration, `len()`, `with` |
| `hasattr(pd, "_x")` / `hasattr(pd, "__x__")`: `False` (raise `AttributeError`) | `<` `<=` `>` `>=` `+` `-` `*` `/`, `isinstance(x, pd.X)`, `issubclass`, `class C(pd.X)` |

Keep out of module level, because they run at import time: decorators from the dependency (`@numba.jit`), subclassing its classes, module-level calls (`boto3.Session()`). Put such code in a module only the optional feature imports.

## More detail

For full API docs see `ref/public-api.md`.
