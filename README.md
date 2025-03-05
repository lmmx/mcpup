# 🐶 mcpup

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
[![PyPI](https://img.shields.io/pypi/v/mcpup.svg)](https://pypi.org/project/mcpup)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/mcpup.svg)](https://pypi.org/project/mcpup)
[![License](https://img.shields.io/pypi/l/mcpup.svg)](https://pypi.python.org/pypi/mcpup)

Automatically generate Pydantic models for all functions in a Python package.

## Features

- **Automatic Function Discovery**: Scans all modules in a package to find functions
- **Pydantic Model Generation**: Creates Pydantic models for function parameters using `pydantic-function-models`
- **Validation**: Generated models perform validation according to type hints
- **Package Structure Preservation**: Maintains the original package's module structure
- **Optional uv Integration**: Can install packages on-the-fly with `uv`

## Installation

```bash
# Install with pip
pip install mcpup

# Or with uv
uv pip install mcpup
```

## Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended)

## Command Line Usage

Generate Pydantic models for all functions in a package:

```bash
mcpup package_name
```

Options:

```
--output, -o DIRECTORY       Directory to save generated models [default: ./mcpup_models]
--install, -i                Install the package using uv before generating models
--include-private            Include private functions (starting with underscore)
--module, -m TEXT            Specific modules to include (can be used multiple times)
--help                       Show help message and exit
```

### Examples

Generate models for all functions in the `polars` package:

```bash
mcpup polars
```

Generate models only for specific modules:

```bash
mcpup polars --module dataframe --module series
```

Install the package first, then generate models:

```bash
mcpup some-package --install
```

Include private functions:

```bash
mcpup mypackage --include-private
```

## Programmatic Usage

You can also use `mcpup` programmatically:

```python
from mcpup.scanner import scan_package
from mcpup.generator import generate_models
from pathlib import Path

# Scan a package for functions
functions = scan_package("mypackage", include_private=False)

# Generate models
output_path = Path("./models")
generate_models(functions, output_path)
```

## Using Generated Models

After generating models, you can use them to validate function arguments:

```python
# Import the generated model
from mcpup_models.mypackage.mymodule import MyFunction

# Validate function arguments
valid_args = MyFunction.model.model_validate({
    "arg1": "value",
    "arg2": 123
})

# Call the function with validated arguments
from mypackage.mymodule import my_function
result = my_function(**valid_args.model_dump(exclude_unset=True))
```

## Contributing

Contributions welcome!

1. **Issues & Discussions**: Please open a GitHub issue or discussion for bugs, feature requests, or questions.
2. **Pull Requests**: PRs are welcome!
   - Install the dev extra with `pip install -e ".[dev]"`
   - Run tests with `pytest`
   - Include updates to docs or examples if relevant

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
