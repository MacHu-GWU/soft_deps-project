# -*- coding: utf-8 -*-

from soft_deps.impl import MissingDependency

import typing as T
import pytest

import copy
import inspect
import pickle
import pydoc
import types


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
    pd = MissingDependency("pandas", error_message="run ``pip install pandas``")
    with pytest.raises(ImportError) as exc_info:
        pd.DataFrame({"a": [1]}).to_excel("output.xlsx")
    assert str(exc_info.value) == (
        "To use `pandas.DataFrame`, run ``pip install pandas``."
    )


@pytest.mark.parametrize(
    "use",
    [
        str,
        iter,
        len,
        lambda missing: missing(1, key="value"),
        lambda missing: missing.attr(),
        lambda missing: missing["key"](),
        lambda missing: f"{missing}",
        lambda missing: missing < 1,
        lambda missing: missing <= 1,
        lambda missing: missing > 1,
        lambda missing: missing >= 1,
        lambda missing: missing + 1,
        lambda missing: missing - 1,
        lambda missing: missing * 1,
        lambda missing: missing / 1,
        lambda missing: 1 in missing,
        lambda missing: isinstance(1, missing),
        lambda missing: issubclass(int, missing),
        lambda missing: types.new_class("Sub", (missing,)),
    ],
)
def test_any_use_raises(use):
    """
    Every real use of the placeholder raises ``ImportError``, so a missing
    dependency is reported at the point of use, not as an unrelated error.
    """
    missing = MissingDependency("important_library")
    with pytest.raises(ImportError):
        use(missing)


def test_with_statement_raises():
    missing = MissingDependency("important_library")
    with pytest.raises(ImportError):
        with missing:
            pass  # pragma: no cover
    with pytest.raises(ImportError):
        missing.__exit__(None, None, None)


def test_type_hints_do_not_raise():
    """
    A module that mentions the dependency only in type hints still imports.
    """
    pd = MissingDependency("pandas")
    npt = MissingDependency("numpy.typing")

    def func(
        df: pd.DataFrame | None = None,
        arr: npt.NDArray[npt.float64] | None = None,
        series: None | pd.Series = None,
    ) -> None:
        pass

    assert inspect.signature(func).parameters["df"].default is None


def test_string_type_hints_can_be_evaluated():
    """
    With ``from __future__ import annotations`` the hints are strings, so the
    import never fails, but tools such as pydantic, typer and Sphinx evaluate
    them with ``typing.get_type_hints()``, which must not raise either.
    """
    pd = MissingDependency("pandas")

    def func(data: "dict") -> "pd.DataFrame | None":
        pass

    hints = T.get_type_hints(func, localns={"pd": pd})
    assert repr(hints["return"]) == "MissingDependency('pandas.DataFrame')"


def test_works_like_a_plain_object():
    """
    Tools that inspect module globals (copy, pickle, inspect, pydoc, hasattr,
    containers) do not trip over the placeholder.
    """
    pd = MissingDependency("pandas")

    assert repr(pd) == "MissingDependency('pandas')"
    assert repr(pd.DataFrame) == "MissingDependency('pandas.DataFrame')"
    assert repr(pd["key"]) == "MissingDependency('pandas[...]')"
    assert bool(pd) is True

    assert hasattr(pd, "__wrapped__") is False
    assert hasattr(pd, "_private") is False
    assert inspect.unwrap(pd) is pd

    assert pd == pd
    assert pd != 1
    assert pd in [pd]
    assert pd in {pd}

    assert repr(copy.copy(pd)) == "MissingDependency('pandas')"
    assert repr(copy.deepcopy(pd)) == "MissingDependency('pandas')"
    assert repr(pickle.loads(pickle.dumps(pd))) == "MissingDependency('pandas')"

    module = types.ModuleType("your_library")
    module.pd = pd
    assert "pd" in pydoc.render_doc(module)


if __name__ == "__main__":
    from soft_deps.tests import run_cov_test

    run_cov_test(
        __file__,
        "soft_deps.impl",
        preview=False,
    )
