# -*- coding: utf-8 -*-

"""
soft-deps is a Python pattern for elegant optional dependency management that
prioritizes developer experience over lazy loading. Unlike true lazy imports,
soft-deps immediately attempts to import dependencies at module load time -
if the dependency is installed, you get the real module with full functionality.
If it's missing, you get a helpful proxy object that provides complete IDE
type hints and auto-completion, but raises informative error messages only
when you actually try to use the missing functionality. This approach gives you
the best of both worlds: seamless development experience with full IDE support
when dependencies are available, and graceful degradation with clear
installation guidance when they're not, all while maintaining zero code
invasiveness in your implementation.
"""

from __future__ import annotations

import typing as T


class MissingDependency:
    """
    Placeholder for an optional dependency that is not installed.

    Using it (calling it, iterating it, converting it to ``str``, comparing it
    with ``<`` or ``>``, doing arithmetic on it, using it in ``isinstance`` or
    as a base class, ...) raises an :class:`ImportError` that tells the user
    how to install it.

    Looking up a public attribute (``pd.DataFrame``), subscripting it
    (``npt.NDArray[np.float64]``), or combining it with ``|``
    (``pd.DataFrame | None``) returns another placeholder instead of raising,
    so a module that only mentions the dependency, such as in a type hint,
    still imports. Private and dunder attributes raise :class:`AttributeError`,
    so ``hasattr()`` and tools such as ``copy``, ``pickle``, ``inspect`` and
    ``pydoc`` treat the placeholder as a plain object.

    :param name: name of the missing dependency, shown in the error message.
    :param error_message: installation hint, shown in the error message.

    .. versionchanged:: 0.2.0

        Attribute access, subscripting and ``|`` return a placeholder instead
        of raising; ``repr()``, ``==`` and ``hash()`` work like on a plain
        object; the error message names the full attribute path.
    """

    def __init__(
        self,
        name: str,
        error_message: str = "please install it",
    ) -> None:
        # Private, so they do not shadow attributes of the real dependency,
        # such as ``pd.name``.
        self._name = name
        self._error_message = error_message

    def _raise_error(self) -> T.NoReturn:
        raise ImportError(f"To use `{self._name}`, {self._error_message}.")

    def _child(self, name: str) -> MissingDependency:
        return MissingDependency(name, self._error_message)

    def __repr__(self) -> str:
        return f"MissingDependency({self._name!r})"

    def __getattr__(self, attr: str) -> MissingDependency:
        # hasattr() and getattr(obj, name, default) only catch AttributeError.
        # Never touch self here: copy and pickle call this before __init__ ran.
        if attr.startswith("_"):
            raise AttributeError(attr)
        return self._child(f"{self._name}.{attr}")

    def __getitem__(self, item) -> MissingDependency:
        return self._child(f"{self._name}[...]")

    def __or__(self, other) -> MissingDependency:
        return self

    def __ror__(self, other) -> MissingDependency:
        return self

    def __call__(self, *args, **kwargs):
        self._raise_error()

    def __str__(self):
        self._raise_error()

    def __iter__(self):
        self._raise_error()

    def __len__(self):
        self._raise_error()

    def __bool__(self) -> bool:
        # Without this, bool() falls back to __len__ and raises.
        return True

    def __enter__(self):
        self._raise_error()

    def __exit__(self, *args):
        self._raise_error()

    def __lt__(self, other):
        self._raise_error()

    def __le__(self, other):
        self._raise_error()

    def __gt__(self, other):
        self._raise_error()

    def __ge__(self, other):
        self._raise_error()

    def __add__(self, other):
        self._raise_error()

    def __sub__(self, other):
        self._raise_error()

    def __mul__(self, other):
        self._raise_error()

    def __truediv__(self, other):
        self._raise_error()

    def __instancecheck__(self, instance):
        self._raise_error()

    def __subclasscheck__(self, subclass):
        self._raise_error()

    def __mro_entries__(self, bases):
        self._raise_error()
