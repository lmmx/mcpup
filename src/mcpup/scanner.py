"""Scanner to find all functions in a Python package."""

import importlib
import inspect
import pkgutil
from collections.abc import Callable
from types import ModuleType


class FunctionInfo:
    """Information about a function to generate a model for."""

    def __init__(
        self,
        function: Callable,
        module_name: str,
        function_name: str,
        docstring: str | None = None,
    ):
        """Initialize a new FunctionInfo instance.

        Args:
            function: The function object
            module_name: Name of the module containing the function
            function_name: Name of the function
            docstring: Function docstring (if available)

        """
        self.function = function
        self.module_name = module_name
        self.function_name = function_name
        self.full_name = f"{module_name}.{function_name}"
        self.docstring = docstring or ""
        self.signature = inspect.signature(function)

    def __repr__(self) -> str:
        """Return string representation of the FunctionInfo object."""
        return f"<FunctionInfo {self.full_name}>"


def scan_package(
    package_name: str,
    include_private: bool = False,
    include_modules: list[str] | None = None,
) -> list[FunctionInfo]:
    """Scan a package and return all functions found within it.

    Args:
        package_name: Name of the package to scan
        include_private: Whether to include private functions (starting with underscore)
        include_modules: Specific modules to include (default: all modules)

    Returns:
        List of FunctionInfo objects for all functions found

    """
    # Try to import the package
    try:
        package = importlib.import_module(package_name)
    except ImportError:
        raise ImportError(f"Could not import package {package_name}. Is it installed?")

    # Set module prefix for filtering
    if include_modules:
        module_prefixes = [f"{package_name}.{mod}" for mod in include_modules]
    else:
        module_prefixes = [package_name]

    functions = []

    # Recursive function to scan modules
    def scan_module(module: ModuleType, module_name: str) -> None:
        # Check if we should scan this module based on prefixes
        if (
            not any(module_name.startswith(prefix) for prefix in module_prefixes)
            and include_modules
        ):
            return

        # Get all functions in this module
        for name, member in inspect.getmembers(module, inspect.isfunction):
            # Skip private functions if not included
            if name.startswith("_") and not include_private:
                continue

            # Check if function is defined in this module (not imported)
            if getattr(member, "__module__", "") == module_name:
                functions.append(
                    FunctionInfo(
                        function=member,
                        module_name=module_name,
                        function_name=name,
                        docstring=inspect.getdoc(member),
                    ),
                )

        # Scan submodules
        if hasattr(module, "__path__"):
            for _, submodule_name, is_pkg in pkgutil.iter_modules(
                module.__path__,
                module.__name__ + ".",
            ):
                try:
                    submodule = importlib.import_module(submodule_name)
                    scan_module(submodule, submodule_name)
                except ImportError:
                    # Skip submodules that can't be imported
                    continue

    # Start scanning from the main package
    scan_module(package, package_name)

    return functions
