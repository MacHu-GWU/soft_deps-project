# -*- coding: utf-8 -*-

"""
Example user script demonstrating soft-deps behavior.

This script shows what happens when a user tries to use a library that
has optional dependencies implemented with the soft-deps pattern.

Scenario 1: important_library is NOT installed

- Code imports and loads successfully (no immediate errors)
- IDE provides full autocomplete and type hints
- Error only occurs when actually trying to use the missing functionality
- Error message is helpful and includes installation instructions

Scenario 2: important_library IS installed

- Everything works seamlessly with no changes to user code
- Full functionality available
"""

from your_library import your_feature

if __name__ == "__main__":
    print("Attempting to use feature that depends on optional library...")
    
    try:
        result = your_feature() # ImportError: To use `important_library`, please install it with: pip install important_library.
        print(f"Success! Result: {result}")
    except ImportError as e:
        print(f"\nCaught expected error: {e}")
        print("\nThis demonstrates the soft-deps pattern:")
        print("- Code imported successfully despite missing dependency")
        print("- IDE had full autocomplete support")
        print("- Clear error message with installation guidance")
        print("- Error only occurred when actually using the functionality")
