.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.2.0 (2026-10-20)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Breaking Changes**

- Drop support for Python 3.9 and 3.10. ``soft_deps`` now requires Python 3.11 or newer.

**Minor Improvements**

- A module that mentions a missing dependency only in type hints now imports. ``def f(df: pd.DataFrame | None)`` no longer raises ``ImportError`` at import time on Python 3.11 to 3.13, and ``typing.get_type_hints()`` (used by pydantic, typer, and Sphinx) works on such hints. Looking up a public attribute, subscripting (``npt.NDArray[np.float64]``), and ``|`` now return another placeholder; the error is raised when the placeholder is actually used.
- The ``ImportError`` message names the full attribute path, such as ``To use `pandas.DataFrame`, pip install pandas.``
- ``len()``, ``with``, ``in``, ``isinstance()``, ``issubclass()``, and using the placeholder as a base class now raise the same ``ImportError`` with the installation hint, instead of an unrelated ``TypeError``.
- Officially support and test on Python 3.11, 3.12, 3.13, and 3.14.

**Bugfixes**

- ``repr()`` of a ``MissingDependency`` no longer raises, so debuggers, pytest output, and ``pydoc`` can display it.
- ``hasattr()`` and ``getattr(obj, name, default)`` on private and dunder names no longer raise ``ImportError``, which crashed ``pytest --doctest-modules``, ``inspect.unwrap()``, and other tools that scan module globals.
- ``copy.copy()`` and ``pickle`` round trips no longer fail with ``RecursionError``.
- ``==``, ``hash()``, and membership in lists and sets now work like on a plain object, instead of raising.
- The placeholder's own ``name`` and ``error_message`` attributes no longer shadow attributes of the real dependency: ``pd.name`` now returns a placeholder for ``pandas.name``.

**Miscellaneous**

- The package no longer defines ``soft_deps.__version__`` and the other ``__author__`` style attributes. Use ``importlib.metadata.version("soft_deps")``.
- Upgrade to the pywf open-source template 2.0.0: uv and mise based tooling, GitHub Actions on Ubuntu and Windows, and the updated Sphinx docs setup.


0.1.1 (2025-06-30)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release
- Add the following public APIs:
    - ``soft_deps.api.MissingDependency``
