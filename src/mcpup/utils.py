"""Utility functions for mcpup."""

import os
import subprocess


def ensure_uv_installed() -> bool:
    """Check if uv is installed and available in the PATH.

    Returns:
        True if uv is installed, False otherwise

    """
    try:
        subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            check=True,
        )
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def run_with_package(package_name: str, command: list) -> subprocess.CompletedProcess:
    """Run a command with a package installed using uv.

    Args:
        package_name: Name of the package to install
        command: Command to run

    Returns:
        CompletedProcess instance with command results

    """
    # Build uvx command
    uvx_command = ["uvx", "--with", package_name] + command

    # Run the command
    return subprocess.run(
        uvx_command,
        capture_output=True,
        text=True,
        check=True,
    )


def sanitize_path(path: str) -> str:
    """Convert a module path to a valid filesystem path.

    Args:
        path: Module path (e.g., 'package.submodule')

    Returns:
        Sanitized path suitable for filesystem use

    """
    return path.replace(".", os.path.sep)
