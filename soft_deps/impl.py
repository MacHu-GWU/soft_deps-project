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


class MissingDependency:
    def __init__(
        self,
        name: str,
        message: str = "please install it",
    ):
        self.name = name
        self.message = message

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

    def __getattr__(self, attr: str):
        raise ImportError(
            f"You didn't install `{self.name}`. To use `{attr}`, {self.message}."
        )
