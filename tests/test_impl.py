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


if __name__ == "__main__":
    from soft_deps.tests import run_cov_test

    run_cov_test(
        __file__,
        "soft_deps.impl",
        preview=False,
    )
