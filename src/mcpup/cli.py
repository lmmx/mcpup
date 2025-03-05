"""CLI interface for mcpup."""

import subprocess
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from mcpup.generator import generate_models
from mcpup.scanner import scan_package
from mcpup.utils import ensure_uv_installed

console = Console()


@click.command(help="Generate Pydantic models for your Python package functions 🐶")
@click.argument("package_name", type=str)
@click.option(
    "--output",
    "-o",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    default=Path("./mcpup_models"),
    help="Directory to save generated models",
)
@click.option(
    "--install",
    "-i",
    is_flag=True,
    help="Install the package using uv before generating models",
)
@click.option(
    "--include-private",
    is_flag=True,
    help="Include private functions (starting with underscore)",
)
@click.option(
    "--module",
    "-m",
    multiple=True,
    help="Specific modules to include (default: all modules)",
)
def cli(
    package_name: str,
    output: Path,
    install: bool,
    include_private: bool,
    module: list[str],
):
    """Generate Pydantic models for all functions in a Python package."""
    console.print(
        Panel.fit(
            "[bold blue]McPup[/] - Pydantic Model Generator 🐶",
            border_style="blue",
        ),
    )

    # Check for uv installation
    if not ensure_uv_installed():
        console.print("[bold red]Error:[/] 'uv' not found. Please install uv first.")
        console.print(
            "Visit https://github.com/astral-sh/uv for installation instructions.",
        )
        sys.exit(1)

    # Install package if requested
    if install:
        console.print(f"Installing {package_name} using uv...")
        try:
            subprocess.run(["uv", "pip", "install", package_name], check=True)
            console.print(f"[green]Successfully installed {package_name}[/]")
        except subprocess.CalledProcessError:
            console.print(f"[bold red]Error:[/] Failed to install {package_name}")
            sys.exit(1)

    try:
        # Ensure output directory exists
        output.mkdir(parents=True, exist_ok=True)

        # Scan package to find all functions
        console.print(f"Scanning package: [bold]{package_name}[/]")
        functions = scan_package(package_name, include_private, module or None)

        if not functions:
            console.print(f"[yellow]No functions found in package {package_name}[/]")
            sys.exit(0)

        console.print(f"Found [bold green]{len(functions)}[/] functions")

        # Generate models
        console.print("Generating Pydantic models...")
        model_files = generate_models(functions, output)

        # Output summary
        console.print(
            f"[bold green]Success![/] Generated {len(model_files)} model files in {output}",
        )

        # Show example usage
        example = f"""
# Example usage:
from mcpup_models.{package_name.replace("-", "_")} import SomeFunction

# Now you can validate function calls
valid_args = SomeFunction.model.model_validate({{"arg1": "value", "arg2": 123}})
result = some_function(**valid_args.model_dump(exclude_unset=True))
"""
        console.print("Example usage:")
        console.print(Syntax(example, "python", theme="monokai", line_numbers=True))

    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
