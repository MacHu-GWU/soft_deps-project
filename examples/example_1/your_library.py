# -*- coding: utf-8 -*-

"""
Example library demonstrating soft-deps pattern.

This module shows how library authors can use soft-deps to create elegant
optional dependency management. Users get full IDE support when dependencies
are available, and helpful error messages when they're missing.
"""

from soft_deps.api import MissingDependency

# Soft dependency pattern: try to import, fallback to proxy if missing
try:
    import important_library  # This could be pandas, numpy, requests, etc.
except ImportError:
    # Create a proxy that provides IDE hints but raises helpful errors when used
    important_library = MissingDependency(
        "important_library", 
        "please install it with: pip install important_library"
    )


def your_feature():
    """
    Example feature that uses an optional dependency.
    
    This function works with full IDE support regardless of whether
    important_library is installed. If the dependency is missing, users
    get a clear error message with installation instructions when they
    actually try to use the functionality.
    
    :returns: Result from important_library's awesome_tool function
    
    :raises ImportError: When important_library is not installed and
        awesome_tool is called
    """
    print("Building feature with important_library...")
    # IDE gets full autocomplete and type hints here, even if library is missing
    # Error only occurs when this line actually executes
    return important_library.awesome_tool()
