
.. image:: https://readthedocs.org/projects/soft-deps/badge/?version=latest
    :target: https://soft-deps.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/soft_deps-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/soft_deps-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/soft_deps-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/soft_deps-project

.. image:: https://img.shields.io/pypi/v/soft-deps.svg
    :target: https://pypi.python.org/pypi/soft-deps

.. image:: https://img.shields.io/pypi/l/soft-deps.svg
    :target: https://pypi.python.org/pypi/soft-deps

.. image:: https://img.shields.io/pypi/pyversions/soft-deps.svg
    :target: https://pypi.python.org/pypi/soft-deps

.. image:: https://img.shields.io/badge/✍️_Release_History!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/soft_deps-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/⭐_Star_me_on_GitHub!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/soft_deps-project

------

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://soft-deps.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/soft_deps-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/soft_deps-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/soft_deps-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/soft-deps#files


Welcome to ``soft_deps`` Documentation
==============================================================================
.. image:: https://soft-deps.readthedocs.io/en/latest/_static/soft_deps-logo.png
    :target: https://soft-deps.readthedocs.io/en/latest/

soft-deps is a Python pattern for elegant optional dependency management that prioritizes developer experience over lazy loading. Unlike true lazy imports, soft-deps immediately attempts to import dependencies at module load time - if the dependency is installed, you get the real module with full functionality. If it's missing, you get a helpful proxy object that provides complete IDE type hints and auto-completion, but raises informative error messages only when you actually try to use the missing functionality.

This approach gives you the best of both worlds: seamless development experience with full IDE support when dependencies are available, and graceful degradation with clear installation guidance when they're not, all while maintaining zero code invasiveness in your implementation.


Quick Start
------------------------------------------------------------------------------
**Why use soft-deps?**

- **For library authors**: Provide optional features without forcing users to install heavy dependencies
- **For users**: Get full IDE support and autocomplete even for optional dependencies  
- **For teams**: Graceful degradation with clear error messages instead of cryptic import failures

**When to use soft-deps?**

Use soft-deps when your library has optional features that depend on external packages:

- Data science libraries with optional visualization (matplotlib, plotly)
- Web frameworks with optional database drivers (psycopg2, pymongo)  
- CLI tools with optional cloud integrations (boto3, google-cloud)
- Any library where you want some features to work without heavy dependencies

**How it works:**

Library authors use the soft-deps pattern in their code:

.. code-block:: python

    # your_library.py
    from soft_deps.api import MissingDependency

    # Try to import optional dependency
    try:
        import pandas as pd
    except ImportError:
        # Create helpful proxy if missing
        pd = MissingDependency("pandas", "pip install pandas")

    def export_to_excel(data):
        """Export data to Excel file (requires pandas)."""
        # IDE gets full autocomplete here even if pandas not installed
        # Error only occurs when this line actually executes
        return pd.DataFrame(data).to_excel("output.xlsx")

Users get seamless experience regardless of what's installed:

.. code-block:: python

    # user_script.py  
    from your_library import export_to_excel

    # This imports successfully even without pandas installed
    # IDE provides full autocomplete and type hints

    try:
        export_to_excel({"col1": [1, 2, 3]})
    except ImportError as e:
        print(e)  # "To use `pandas.DataFrame`, pip install pandas."

**The difference:**

.. code-block:: python

    # ❌ Traditional approach - breaks immediately  
    import pandas as pd  # ImportError if not installed
    
    # ❌ Lazy imports - no IDE support
    def export_data():
        import pandas as pd  # IDE can't help with autocomplete
    
    # ✅ soft-deps - best of both worlds
    try:
        import pandas as pd
    except ImportError:
        pd = MissingDependency("pandas", "pip install pandas")
    # IDE gets full support, graceful errors when actually used


Recommended Layout
------------------------------------------------------------------------------
Put every optional import in one module, and import the names from there. The installation hint can point at the extra that brings the dependency in:

.. code-block:: python

    # your_library/importer.py
    from soft_deps.api import MissingDependency

    try:
        import pandas as pd
    except ImportError:
        pd = MissingDependency("pandas", "pip install your_library[excel]")

    try:
        import boto3
    except ImportError:
        boto3 = MissingDependency("boto3", "pip install your_library[aws]")

.. code-block:: python

    # your_library/excel.py
    from .importer import pd

    def export_to_excel(data: dict, path: str) -> pd.DataFrame:
        df = pd.DataFrame(data)
        df.to_excel(path)
        return df

The rule is simple: **use the dependency inside functions, not at module level.** Then importing ``your_library.excel`` always works, and only calling ``export_to_excel()`` without pandas raises an ``ImportError``.


What Raises and What Does Not
------------------------------------------------------------------------------
Only real use of the missing dependency raises an ``ImportError``. Merely mentioning it does not, so type hints work with or without ``from __future__ import annotations``:

.. list-table::
    :header-rows: 1

    * - Does not raise
      - Raises ``ImportError``
    * - ``pd.DataFrame``, ``npt.NDArray[np.float64]``, ``pd.DataFrame | None`` (each returns another placeholder, so type hints and ``typing.get_type_hints()`` work)
      - calling: ``pd.DataFrame(data)``, ``pd.read_csv(path)``
    * - ``repr(pd)``, ``pd == other``, ``hash(pd)``, ``pd in some_list``, ``copy.copy(pd)``, ``pickle.dumps(pd)``, ``hasattr(pd, "__wrapped__")``
      - ``str(pd)``, ``f"{pd}"``, ``for x in pd``, ``len(pd)``, ``with pd:``
    * - ``if pd:`` (always true, like a real module)
      - ``<``, ``>``, ``+``, ``-``, ``*``, ``/``, ``isinstance(x, pd.DataFrame)``, ``class MyFrame(pd.DataFrame)``

The error message names what was used, for example ``To use `pandas.DataFrame`, pip install your_library[excel].``

**Keep these out of module level**, because they run while the module is imported:

- decorators from the dependency, such as ``@numba.jit``;
- classes that subclass something from the dependency, such as ``class MyModel(pydantic.BaseModel)``;
- module-level calls, such as ``session = boto3.Session()``.

Put such code in a module that only the optional feature imports.


.. _install:

Install
------------------------------------------------------------------------------

``soft_deps`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install soft-deps

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade soft-deps


.. _use-with-ai-coding-agents:

Use with AI Coding Agents
------------------------------------------------------------------------------

This repo ships an `Agent Skill <https://code.claude.com/docs/en/skills>`_ that documents the public API of ``soft_deps``, so an AI coding agent such as Claude Code can use the library without reading its source. It lives in `.claude/skills/pypi-soft_deps <https://github.com/MacHu-GWU/soft_deps-project/tree/main/.claude/skills/pypi-soft_deps>`_. To use it in your project, copy it into your project's ``.claude/skills/`` folder. Run this from your project's root:

.. code-block:: console

    $ git clone --depth 1 https://github.com/MacHu-GWU/soft_deps-project.git /tmp/soft_deps-project
    $ mkdir -p .claude/skills
    $ cp -R /tmp/soft_deps-project/.claude/skills/pypi-soft_deps .claude/skills/
