# Data Model: CLI Application Foundation

**Feature**: 001-cli-scaffolding
**Date**: 2026-02-14
**Source**: Extracted from spec.md requirements + research.md Typer patterns

## Overview

This feature establishes the CLI application structure using Typer and Rich. The "data model" for CLI infrastructure consists of the application's structural components rather than persistent data entities.

---

## Core Entities

### 1. CLIApp

**Purpose**: Root application instance that coordinates command execution

**Type**: Typer application instance

**Configuration**:

| Property | Type | Value | Description |
|----------|------|-------|-------------|
| `name` | str | "ram" | Application name shown in help |
| `help` | str | Description text | Main help message |
| `add_completion` | bool | False | Shell completion (disabled for prototype) |
| `no_args_is_help` | bool | True | Show help when no args provided |
| `rich_markup_mode` | str | "rich" | Enable Rich formatting in help |

**Responsibilities**:
- Register commands and command groups
- Handle global options (--version, --help)
- Coordinate Rich console instance
- Manage application lifecycle (startup, shutdown)

**Example**:
```python
app = typer.Typer(
    name="ram",
    help="Ragged Memory - Semantic memory for LLMs",
    add_completion=False,
    no_args_is_help=True
)
```

---

### 2. Command

**Purpose**: Executable action invoked by users (e.g., `ram hello`)

**Structure**:

| Component | Type | Description |
|-----------|------|-------------|
| Function | Callable | Python function decorated with `@app.command()` |
| Name | str | Command name (defaults to function name) |
| Help | str | Function docstring (shown in help) |
| Parameters | List[Parameter] | Arguments and options |

**Validation Rules**:
- Function name must be valid Python identifier (becomes command name)
- Must have docstring (used for help text)
- Parameters must have type hints (Typer uses for validation)
- Must handle errors gracefully or let them propagate

**Example**:
```python
@app.command()
def hello(name: str = typer.Argument("World")):
    """
    Say hello to someone.

    Args:
        name: The name to greet
    """
    console.print(f"[green]Hello, {name}![/green]")
```

**Invocation**: `ram hello John` → outputs "Hello, John!"

---

### 3. Argument

**Purpose**: Required positional input for a command

**Definition Pattern**:
```python
name: str = typer.Argument(..., help="Description")
```

**Properties**:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| Type annotation | type | Yes | Python type (str, int, float, Path, etc.) |
| Default value | any | No | Default if not provided (or `...` for required) |
| Help text | str | Yes | Description shown in command help |
| Validation | Callable | No | Custom validator function |

**Validation**:
- Typer validates type automatically
- Required if default is `...`
- Optional if default value provided

**Examples**:
```python
# Required argument
content: str = typer.Argument(..., help="Memory content to store")

# Optional argument with default
name: str = typer.Argument("World", help="Name to greet")

# Validated argument
count: int = typer.Argument(..., min=1, max=100, help="Number of items")
```

---

### 4. Option

**Purpose**: Optional flag that modifies command behavior

**Definition Pattern**:
```python
flag: bool = typer.Option(False, "--flag", "-f", help="Description")
```

**Properties**:

| Property | Type | Description |
|----------|------|-------------|
| Default value | any | Value if flag not provided |
| Long name | str | Full flag name (e.g., `--verbose`) |
| Short name | str | Optional single-letter alias (e.g., `-v`) |
| Help text | str | Description in help output |
| Callback | Callable | Function to run when flag is set |
| Is eager | bool | Process before other options |

**Types of Options**:

1. **Boolean flags**: Present = True, Absent = False
   ```python
   verbose: bool = typer.Option(False, "--verbose", "-v")
   ```

2. **Value options**: Accept arguments
   ```python
   output: Path = typer.Option(None, "--output", "-o", help="Output file")
   ```

3. **Eager options**: Process first (e.g., --version, --help)
   ```python
   version: bool = typer.Option(
       None,
       "--version",
       callback=version_callback,
       is_eager=True
   )
   ```

---

### 5. Console (Rich)

**Purpose**: Formatted output manager for terminal display

**Type**: Rich Console instance (singleton)

**Capabilities**:

| Feature | Method | Usage |
|---------|--------|-------|
| Colored text | `print("[color]text[/color]")` | Semantic colors for output |
| Tables | `Table()` | Structured data display |
| Panels | `Panel()` | Boxed important messages |
| Syntax highlight | `Syntax()` | Code/JSON highlighting |
| Progress bars | `Progress()` | Long operations feedback |

**Standard Colors**:
- `[green]` - Success messages
- `[red]` - Error messages
- `[yellow]` - Warnings
- `[blue]` - Informational
- `[cyan]` - Highlights
- `[dim]` - Secondary info

**Example Usage**:
```python
from rich.console import Console
console = Console()

# Simple output
console.print("[green]Success![/green]")

# Error with panel
console.print(Panel("[red]Error: File not found[/red]", title="Error"))

# Table
table = Table(title="Results")
table.add_column("ID", style="cyan")
table.add_column("Content")
console.print(table)
```

---

## Application Structure Model

### Entry Point Flow

```
User runs: ram [OPTIONS] COMMAND [ARGS]
     │
     ├─> __main__.py: main()
     │       │
     │       └─> cli/app.py: app()
     │               │
     │               ├─> Typer parses arguments
     │               ├─> Validates types
     │               ├─> Processes eager options (--version, --help)
     │               └─> Routes to command function
     │                       │
     │                       └─> Command executes
     │                               │
     │                               └─> Uses Rich console for output
     │
     └─> Exit with code (0=success, 1=error)
```

### Command Registration Pattern

```python
# cli/app.py
app = typer.Typer(...)
console = Console()

# Future features register commands:
from ram.cli.commands import demo
app.add_typer(demo.app, name="demo")

# Or register individual commands:
from ram.cli.commands.demo import hello
app.command()(hello)
```

---

## Validation Rules

### Global Validation

- All commands must have docstrings (for help generation)
- All parameters must have type hints (for Typer validation)
- All options must have help text
- Exit codes: 0 (success), 1 (error), 2 (usage error)

### Type Validation

Typer automatically validates:
- `str` - any string
- `int` - must be integer
- `float` - must be float
- `bool` - flags (presence = True)
- `Path` - converts to pathlib.Path
- `Enum` - must be valid enum value

### Error Handling

**Pattern**:
```python
try:
    # Command logic
    console.print("[green]Success![/green]")
except ValueError as e:
    console.print(f"[red]Error:[/red] {e}")
    raise typer.Exit(code=1)
except Exception as e:
    console.print(f"[red]Unexpected error:[/red] {e}")
    raise  # Let it crash (prototype approach)
```

**Rules**:
- Expected errors: catch, show message, exit with code 1
- Unexpected errors: let Python crash (per constitution)
- Always use Rich formatting for error messages
- Be specific: what went wrong + how to fix

---

## Help System Model

### Help Hierarchy

1. **Application Help** (`ram --help`):
   - Application description
   - Global options (--version, --help)
   - List of available commands

2. **Command Help** (`ram command --help`):
   - Command description (docstring)
   - Arguments (positional params)
   - Options (flags)
   - Usage examples (if provided)

### Help Generation Rules

- Typer auto-generates from docstrings and type hints
- Rich formatting applied automatically
- Use numpy-style docstrings for clarity:
  ```python
  def command(arg: str):
      """
      Brief description.

      Longer description with details.

      Args:
          arg: Description of argument

      Examples:
          $ ram command value
      """
  ```

---

## Version Management

**Version String**:
- Defined in `version.py`: `__version__ = "0.1.0"`
- Semantic versioning: MAJOR.MINOR.PATCH
- Displayed via `--version` flag

**Version Callback**:
```python
def version_callback(value: bool):
    if value:
        console.print(f"Ragged Memory (RAM) version {__version__}")
        raise typer.Exit()
```

**Registered as eager option**:
```python
@app.callback()
def main(
    version: bool = typer.Option(
        None, "--version", "-v",
        callback=version_callback,
        is_eager=True
    )
):
    pass
```

---

## Package Metadata Model

**pyproject.toml structure**:

```toml
[project]
name = "ragged-memory"
version = "0.1.0"  # Matches version.py
description = "Semantic memory for LLMs at the command line"
requires-python = ">=3.11"
dependencies = ["typer[all]>=0.9.0"]

[project.scripts]
ram = "ram.__main__:main"  # Creates `ram` command
```

**Entry Point**:
- Script name: `ram`
- Module: `ram.__main__`
- Function: `main()`

---

## State & Lifecycle

### Application State

**Stateless Design**:
- CLI app holds no persistent state
- Each command invocation is independent
- No global mutable state

### Lifecycle Events

1. **Startup**: Import app, create console
2. **Parse**: Typer parses args/options
3. **Validate**: Type checking, required args
4. **Execute**: Run command function
5. **Exit**: Return exit code

**No initialization required** - Typer handles lifecycle automatically.

---

## Extension Points (Future Features)

### Adding New Commands

```python
# commands/store.py
import typer
app = typer.Typer()

@app.command()
def add(content: str):
    """Store a memory."""
    # Implementation here
    pass

# In cli/app.py:
from ram.cli.commands import store
main_app.add_typer(store.app, name="store")
```

### Adding Global Options

```python
@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v")
):
    """Main callback with global options."""
    if verbose:
        console.print("[dim]Verbose mode enabled[/dim]")
```

---

## Summary

**Core Components**:
1. **CLIApp** - Typer application instance
2. **Command** - Decorated Python functions
3. **Argument** - Required positional inputs
4. **Option** - Optional flags
5. **Console** - Rich output manager

**Principles**:
- Type-driven design (Typer validates from type hints)
- Help auto-generation (docstrings → help text)
- Clean output (Rich formatting)
- Fail fast (let errors surface, show clearly)

**Ready for**: CLI contract definitions and quickstart guide
