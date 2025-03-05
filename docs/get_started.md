---
title: "Get Started"
icon: material/human-greeting
---

# Getting Started

## 1. Installation

`mcpup` is [on PyPI](https://pypi.org/project/mcpup). Install with:

```bash
pip install mcpup
```

!!! info "Using `uv` (optional)"
    If you set up [uv](https://docs.astral.sh/uv/getting-started/installation/) (recommended for a smoother developer experience), you can install with:
    ```bash
    uv pip install mcpup
    ```
    or set up a project (e.g., `uv init --app --package`, `uv venv`, then activate the venv), and add `mcpup`:
    ```bash
    uv add mcpup
    ```

## 2. Usage

`mcpup` provides a CLI tool to generate Pydantic models for all functions in a Python package. To generate models for a package:

```bash
mcpup package_name
```

This will scan the package and create validated Pydantic models for all public functions.

!!! tip "Install the package first"
    If the package isn't already installed, use the `--install` flag:
    ```bash
    mcpup package_name --install
    ```

### More CLI Examples

- **Generate models for a specific module within a package**:
  ```bash
  mcpup pandas --module core --module dataframe
  ```

- **Include private functions (those starting with underscore)**:
  ```bash
  mcpup requests --include-private
  ```

- **Specify a custom output directory**:
  ```bash
  mcpup polars --output ./my_models
  ```

For the complete list of options, run:

```bash
mcpup --help
```

## 3. Local Development

1. **Clone the Repo**:
   ```bash
   git clone https://github.com/lmmx/mcpup.git
   ```

2. **Install Dependencies**:
   - If you're using [pdm](https://pdm.fming.dev/latest/):
     ```bash
     pdm install
     ```
   - Otherwise, standard pip:
     ```bash
     pip install -e .
     ```

3. **Optional: Pre-commit Hooks**:
   ```bash
   pre-commit install
   ```
   This automatically runs lint checks (e.g., ruff) before each commit.

4. **Run Tests**:
   ```bash
   pytest
   ```

5. **Build/Serve Docs** (if included):
   ```bash
   mkdocs serve
   ```
   Then visit the local server link. Use `mkdocs gh-deploy` to publish on GitHub Pages.

## 4. Example Workflow

Let's walk through a complete example using `mcpup` to generate models for the popular `requests` library:

1. **Install mcpup and the target package**:
   ```bash
   pip install mcpup requests
   ```

2. **Generate models for all functions in the package**:
   ```bash
   mcpup requests -o ./requests_models
   ```

3. **Use the generated models in your code**:
   ```python
   from requests_models.requests.api import Get

   # Validate parameters for requests.get
   params = Get.model.model_validate({
       "url": "https://api.github.com/users/octocat",
       "params": {"page": 1},
       "headers": {"Accept": "application/json"}
   })

   # Call the function with validated parameters
   import requests
   response = requests.get(**params.model_dump(exclude_unset=True))
   ```

4. **Inspect model validation errors**:
   ```python
   try:
       # This will fail validation (timeout should be a float or int)
       params = Get.model.model_validate({
           "url": "https://api.github.com/users/octocat",
           "timeout": "not-a-number"
       })
   except Exception as e:
       print(f"Validation error: {e}")
   ```

## 5. How It Works

`mcpup` operates by:

1. **Scanning the package**: Uses Python's `importlib` and `inspect` to find all functions
2. **Analyzing signatures**: Examines type hints, defaults, and parameter kinds
3. **Generating models**: Creates Pydantic models that match function signatures
4. **Preserving structure**: Maintains the package's module hierarchy in the generated code

The generated models can be used to:

- Validate function arguments before calling functions
- Document function parameters with proper type information
- Generate OpenAPI schemas for Python functions
- Test function calls with different parameter sets

## 6. Configuration

`mcpup` has sensible defaults but can be customized with CLI options:

- **Output directory**: Where to save generated models (default: `./mcpup_models`)
- **Module filtering**: Generate models only for specific modules
- **Private functions**: Option to include private functions (starting with `_`)
- **Uv integration**: Can install packages automatically using `uv`

For further details, consult the [API Reference](api/index.md) or the help text:

```bash
mcpup --help
```
