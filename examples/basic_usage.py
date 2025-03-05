"""Example usage of mcpup to generate Pydantic models for a package."""

import os
import sys
from pathlib import Path

# Add parent directory to path to import mcpup
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mcpup.generator import generate_models
from mcpup.scanner import scan_package

# Replace with the name of the package you want to generate models for
PACKAGE_NAME = "requests"


def main():
    """Run the example to demonstrate mcpup functionality."""
    print(f"Scanning package: {PACKAGE_NAME}")

    # Scan the package to find all functions
    functions = scan_package(PACKAGE_NAME, include_private=False)

    print(f"Found {len(functions)} functions")

    # Print the first 5 functions found
    print("\nSample of functions found:")
    for func in functions[:5]:
        print(f"- {func.full_name}")

    # Set output directory
    output_dir = Path("./generated_models")

    # Generate models
    print(f"\nGenerating models in {output_dir}")
    model_files = generate_models(functions, output_dir)

    print(f"Generated {len(model_files)} files")

    # Print example usage
    print("\nExample usage:")
    example = f"""
from generated_models.{PACKAGE_NAME} import SomeFunction

# Validate function arguments
valid_args = SomeFunction.model.model_validate({{"arg1": "value", "arg2": 123}})

# Call the function with validated arguments
from {PACKAGE_NAME} import some_function
result = some_function(**valid_args.model_dump(exclude_unset=True))
"""
    print(example)


if __name__ == "__main__":
    main()
