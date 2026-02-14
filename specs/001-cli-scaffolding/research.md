# Research: CLI Application Foundation

**Feature**: 001-cli-scaffolding
**Date**: 2026-02-14
**Purpose**: Research Typer + Rich best practices for modern CLI foundation

## Research Question 1: Typer App Structure & Organization

**Decision**: Use single Typer app instance with command registration pattern

**Rationale**:
- Typer's recommended pattern: create app in one place, register commands elsewhere
- Enables modular command addition (future features just import and register)
- Clean separation: app setup vs command implementations
- Supports command groups naturally

**Pattern**:
```python
# cli/app.py
import typer
from rich.console import Console

app = typer.Typer(
    name="ram",
    help="Ragged Memory - Semantic memory for LLMs at the command line",
    add_completion=False,  # Disable for prototype simplicity
)
console = Console()

# Future features add commands:
# from ram.cli.commands import store, search
# app.add_typer(store.app, name="store")
```

**Alternatives Considered**:
- Multiple Typer apps - unnecessary complexity for single CLI
- Decorators directly on main app - harder to organize as commands grow
- Click directly - Typer is simpler with better type support

---

## Research Question 2: Rich Integration Patterns

**Decision**: Create shared Rich Console instance, use throughout CLI

**Rationale**:
- Rich Console provides: colors, formatting, tables, panels, progress
- Single console instance ensures consistent styling
- Can customize theme/style in one place
- Typer automatically uses Rich if installed

**Usage Pattern**:
```python
# Typer automatically uses Rich for output if installed
from rich.console import Console
from rich.table import Table

console = Console()

# In commands:
console.print("[green]Success![/green]")
console.print("[red]Error:[/red] Something went wrong")

# Tables for structured output:
table = Table(title="Memories")
table.add_column("ID", style="cyan")
table.add_column("Content", style="white")
console.print(table)
```

**Rich Features to Use**:
- **Colors/Styles**: Semantic colors (green=success, red=error, yellow=warning, blue=info)
- **Panels**: Box important information
- **Tables**: Structured data display
- **Syntax**: Code/JSON highlighting (for future features)
- **Progress**: For long operations (future)

**Alternatives Considered**:
- Plain print() - loses formatting, less user-friendly
- ANSI codes directly - reinventing the wheel, hard to maintain
- Other libraries (colorama, termcolor) - Rich is most comprehensive

---

## Research Question 3: Package Structure & Entry Points

**Decision**: Use `pyproject.toml` with modern Python packaging

**Rationale**:
- `pyproject.toml` is modern standard (PEP 517/518/621)
- Cleaner than setup.py
- Supports entry points for `ram` command
- Works with pip, pipx, poetry, etc.

**Configuration**:
```toml
[build-system]
requires = ["setuptools>=65.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "ragged-memory"
version = "0.1.0"
description = "Semantic memory for LLMs at the command line"
requires-python = ">=3.11"
dependencies = [
    "typer[all]>=0.9.0",   # [all] includes Rich automatically
]

[project.scripts]
ram = "ram.__main__:main"
```

**Entry Point**:
```python
# ram/__main__.py
from ram.cli.app import app

def main():
    app()

if __name__ == "__main__":
    main()
```

**Alternatives Considered**:
- setup.py - legacy, more verbose
- setup.cfg - transitional format, less standard than pyproject.toml
- No package - harder to install, no `ram` command

---

## Research Question 4: Command Organization Patterns

**Decision**: Commands directory with one file per command (or command group)

**Rationale**:
- Scales naturally: new features add new command files
- Clear organization: `commands/store.py`, `commands/search.py`
- Follows constitution principle IV (one class per file)
- Easy to find and modify commands

**Pattern**:
```python
# commands/demo.py (for this scaffolding feature)
import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def hello(name: str = typer.Argument("World")):
    """Say hello to someone."""
    console.print(f"[green]Hello, {name}![/green]")

# Main app registers this:
# from ram.cli.commands import demo
# main_app.add_typer(demo.app, name="demo")
```

**Alternatives Considered**:
- All commands in one file - doesn't scale, violates constitution
- Commands in separate package - over-engineering for prototype
- Classes instead of functions - unnecessary for simple commands

---

## Research Question 5: Help & Version Handling

**Decision**: Use Typer's built-in help generation + custom version callback

**Rationale**:
- Typer auto-generates help from docstrings and type hints
- Rich formatting applied automatically
- Version via callback pattern (Typer convention)

**Implementation**:
```python
# version.py
__version__ = "0.1.0"

# app.py
from ram.version import __version__

def version_callback(value: bool):
    if value:
        console.print(f"Ragged Memory (RAM) version {__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit"
    )
):
    """
    Ragged Memory (RAM) - Semantic memory for LLMs at the command line.

    Store information once, retrieve it later by meaning.
    """
    pass
```

**Help Output** (Typer generates automatically):
```
Usage: ram [OPTIONS] COMMAND [ARGS]...

  Ragged Memory (RAM) - Semantic memory for LLMs at the command line.

  Store information once, retrieve it later by meaning.

Options:
  -v, --version          Show version and exit
  --help                 Show this message and exit

Commands:
  demo  Demo command (placeholder for future features)
```

**Alternatives Considered**:
- Manual help formatting - Typer does it better
- Argparse - less modern, more boilerplate
- Click directly - Typer is cleaner

---

## Research Question 6: Error Handling Patterns

**Decision**: Let Typer handle validation errors, use Rich for custom errors

**Rationale**:
- Typer automatically validates types and required args
- Shows helpful error messages with suggestions
- For custom errors: use Rich console to format clearly
- Prototype approach: fail fast, show clear message (per constitution)

**Pattern**:
```python
# Typer handles basic errors automatically:
@app.command()
def example(count: int):
    """Example command."""
    # If user passes non-integer: Typer shows error automatically

# For custom errors:
from rich.console import Console
console = Console()

def my_command():
    try:
        # ... some operation
    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] File not found: {e.filename}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        raise typer.Exit(code=1)
```

**Error Display Strategy**:
- Use Rich colors: `[red]` for errors, `[yellow]` for warnings
- Be specific: tell user exactly what went wrong
- Exit with non-zero code for errors (convention)
- Don't catch everything - let Python crashes happen (prototype approach)

**Alternatives Considered**:
- Try/except everywhere - over-engineering for prototype
- Custom error classes - unnecessary abstraction
- Logging framework - overkill for CLI tool

---

## Best Practices Summary: Typer + Rich CLI

### Command Design
- Use type hints: Typer converts to validation automatically
- Write docstrings: Typer shows them in help
- Default values with `typer.Option()` or `typer.Argument()`
- Use descriptive parameter names: they become CLI flags

### Output Design
- Consistent colors: green=success, red=error, yellow=warning, blue=info
- Use Rich tables for structured data
- Use Rich panels for important messages
- Progress bars for long operations (future)

### User Experience
- Help should be discoverable: `ram --help`, `ram command --help`
- Error messages should be actionable: what went wrong + how to fix
- Commands should be verb-based: `ram store`, `ram search`
- Output should be parseable (future: add `--json` flag)

---

## Python Package Management

**Installation Methods**:

1. **Development (pip editable install)**:
   ```bash
   cd ragged_memory
   pip install -e .
   # Now `ram` command is available
   ```

2. **User install (pipx)**:
   ```bash
   pipx install /path/to/ragged_memory
   # Isolates dependencies, installs `ram` command
   ```

3. **Direct (poetry/pip)**:
   ```bash
   pip install .
   ```

**Dependencies to Install**:
- `typer[all]>=0.9.0` - includes Rich automatically
- No other dependencies needed for scaffolding feature

---

## Implementation Checklist

For this scaffolding feature, implement:

1. ✅ **Package structure**: `ram/` package with `__init__.py`, `__main__.py`
2. ✅ **pyproject.toml**: Package metadata, dependencies, entry point
3. ✅ **cli/app.py**: Typer app instance, version callback, main callback
4. ✅ **version.py**: Version string constant
5. ✅ **commands/__init__.py**: Empty (future commands register here)
6. ✅ **README.md**: Installation and usage instructions
7. ✅ **Demo command**: Simple "hello" command to prove it works

**Out of scope** (per constitution):
- ❌ Tests (not required for prototype)
- ❌ Auto-completion (future enhancement)
- ❌ Configuration files (future feature)
- ❌ Logging infrastructure (not needed yet)

---

## Research Summary

**Technology Stack**:
- Python 3.11+ with modern type hints
- Typer 0.9+ for CLI framework
- Rich 13+ for beautiful terminal output

**Architecture Pattern**:
- Single Typer app instance
- Modular command registration
- Shared Rich console
- Entry point via pyproject.toml

**Development Approach**:
- Start with minimal scaffolding
- Add demo command to prove it works
- Future features add commands by importing

**Ready for Phase 1**: Design data models and CLI contracts
