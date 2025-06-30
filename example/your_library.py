# -*- coding: utf-8 -*-

from soft_deps.api import MissingDependency

try:
    import important_library
except ImportError:
    important_library = MissingDependency("important_library")


def your_feature():
    print("using important_library to build a feature")
    return important_library.awesome_tool()
