# -*- coding: utf-8 -*-


from soft_deps.api import MissingDependency

try:
    from magic_pandas import DataFrame
except ImportError:
    DataFrame = MissingDependency(
        "DataFrame", "please install it with: pip install magic_pandas"
    )


def your_feature():
    print("Building feature with important_library...")
    return DataFrame()
