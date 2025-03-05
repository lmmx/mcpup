"""Generator for Pydantic models based on function signatures."""

from pathlib import Path

from pydantic_function_models import ValidatedFunction

from mcpup.scanner import FunctionInfo


def _sanitize_module_name(name: str) -> str:
    """Convert module name to valid Python identifier."""
    return name.replace("-", "_").replace(".", "_")


def generate_model_code(function_info: FunctionInfo) -> str:
    """Generate Python code for a Pydantic model based on a function.

    Args:
        function_info: Information about the function

    Returns:
        Generated Python code as a string

    """
    try:
        # Create a ValidatedFunction instance to ensure it can be created
        # (We don't use the instance directly, but this validates the function can be modeled)
        ValidatedFunction(function_info.function)

        # Generate import statements
        imports = [
            "from typing import Any, Dict, List, Optional, Union, Tuple",
            "from pydantic import BaseModel, Field",
            "from pydantic_function_models import ValidatedFunction",
        ]

        # Get the function's module and name
        module_name = function_info.module_name
        func_name = function_info.function_name

        # Create a class name based on the function name
        # Convert snake_case to PascalCase
        class_name = "".join(word.capitalize() for word in func_name.split("_"))

        # Format the docstring
        docstring = function_info.docstring
        if docstring:
            # Fix escape sequences in docstrings
            docstring = docstring.replace("\\*", "\\\\*")
            docstring = docstring.replace("\\[", "\\\\[")
            docstring = docstring.replace("\\]", "\\\\]")
            # Indent docstring for class definition
            docstring = "\n    ".join(docstring.split("\n"))
            class_docstring = f'    """{docstring}"""'
        else:
            class_docstring = '    """Pydantic model for function parameters."""'

        # Create the class definition
        class_def = f"""
class {class_name}:
{class_docstring}

    # Original function signature: {str(function_info.signature)}
    # Module: {module_name}

    @staticmethod
    def get_original_function():
        \"\"\"Get the original function this model is based on.\"\"\"
        import {module_name}
        return {module_name}.{func_name}

    model = ValidatedFunction({module_name}.{func_name}).model
"""

        # Combine everything
        model_code = "\n".join(imports) + "\n" + class_def

        return model_code

    except Exception as e:
        return f"""
# Failed to generate model for {function_info.full_name}
# Error: {str(e)}
"""


def generate_models(functions: list[FunctionInfo], output_dir: Path) -> list[Path]:
    """Generate Pydantic models for all functions and save them to files.

    Args:
        functions: List of functions to generate models for
        output_dir: Directory to save generated models

    Returns:
        List of paths to generated model files

    """
    # Create a directory structure based on modules
    generated_files = []

    # Group functions by module
    modules: dict[str, list[FunctionInfo]] = {}
    for func in functions:
        if func.module_name not in modules:
            modules[func.module_name] = []
        modules[func.module_name].append(func)

    # Create __init__.py to make the output directory a package
    init_path = output_dir / "__init__.py"
    with open(init_path, "w") as f:
        f.write('"""Generated Pydantic models for package functions."""\n')
    generated_files.append(init_path)

    # Generate model files for each module
    for module_name, module_functions in modules.items():
        # Create module path
        parts = module_name.split(".")
        module_dir = output_dir

        # Create directory structure
        for part in parts:
            module_dir = module_dir / part
            module_dir.mkdir(exist_ok=True)

            # Create __init__.py in each directory
            init_path = module_dir / "__init__.py"
            if not init_path.exists():
                with open(init_path, "w") as f:
                    f.write(f'"""Models for {part} module."""\n')
                generated_files.append(init_path)

        # Generate models.py file containing all models for this module
        model_file = module_dir / "models.py"

        # Create the model file
        with open(model_file, "w") as f:
            f.write(f'"""Pydantic models for {module_name} functions."""\n\n')

            # Import the module
            f.write(f"import {module_name}\n\n")

            # Generate model for each function
            for func_info in module_functions:
                f.write(generate_model_code(func_info))
                f.write("\n\n")

            # Export all models
            export_names = [
                "".join(word.capitalize() for word in func.function_name.split("_"))
                for func in module_functions
            ]
            f.write(f"__all__ = {repr(export_names)}\n")

        generated_files.append(model_file)

        # Update __init__.py to import and expose the models
        with open(module_dir / "__init__.py", "a") as f:
            f.write("\n# Import all models\n")
            f.write("from .models import *  # noqa\n")

    return generated_files
