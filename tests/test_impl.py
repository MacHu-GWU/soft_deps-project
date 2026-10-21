# -*- coding: utf-8 -*-

from soft_deps.impl import MissingDependency

import typing as T
import pytest


def test():
    try:
        if T.TYPE_CHECKING:
            from soft_deps.tests import important_library
        raise ImportError
    except ImportError:
        important_library = MissingDependency("important_library")

    with pytest.raises(ImportError):
        # IDE auto complete should work, but will raise ImportError
        important_library.important_function()


def test_error_message():
    missing = MissingDependency(
        "important_library",
        error_message="run ``pip install important_library``",
    )
    with pytest.raises(ImportError) as exc_info:
        missing.important_function()
    assert str(exc_info.value) == (
        "To use `important_library`, run ``pip install important_library``."
    )


@pytest.mark.parametrize(
    "use",
    [
        repr,
        hash,
        iter,
        lambda missing: missing.attr,
        lambda missing: missing["key"],
        lambda missing: missing(1, key="value"),
        lambda missing: missing == 1,
        lambda missing: missing < 1,
        lambda missing: missing <= 1,
        lambda missing: missing > 1,
        lambda missing: missing >= 1,
        lambda missing: missing + 1,
        lambda missing: missing - 1,
        lambda missing: missing * 1,
        lambda missing: missing / 1,
    ],
)
def test_any_use_raises(use):
    """
    Every way of using the placeholder raises ``ImportError``, so a missing
    dependency is reported at the point of use, not as an unrelated error.
    """
    missing = MissingDependency("important_library")
    with pytest.raises(ImportError):
        use(missing)


if __name__ == "__main__":
    from soft_deps.tests import run_cov_test

    run_cov_test(
        __file__,
        "soft_deps.impl",
        preview=False,
    )
