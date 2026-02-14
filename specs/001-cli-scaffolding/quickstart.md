# Quickstart: CLI Application Foundation

**Feature**: 001-cli-scaffolding
**Date**: 2026-02-14
**Purpose**: Get started using and extending the RAM CLI framework

## Installation

### Prerequisites

- Python 3.11 or later
- pip or pipx

### Install for Development

```bash
# Clone the repository (if not already done)
cd ragged_memory

# Install in editable mode
pip install -e .

# Verify installation
ram --version
ram --help
```

**Expected output**:
```
Ragged Memory (RAM) version 0.1.0
```

### Install for Users (pipx recommended)

```bash
# Install with pipx (isolated environment)
pipx install /path/to/ragged_memory

# Or with pip
pip install /path/to/ragged_memory
```

---

## Basic Usage

### Get Help

```bash
# Application help
ram --help

# Command-specific help
ram hello --help
```

### Run Demo Command

```bash
# Basic hello
ram hello
# Output: Hello, World!

# Hello with name
ram hello Alice
# Output: Hello, Alice!
```

### Check Version

```bash
ram --version
# Output: Ragged Memory (RAM) version 0.1.0
```

---

## For Developers: Adding New Commands

This CLI framework is designed to be easily extensible. Here's how to add new commands for future features.

### Quick Add: Single Command

**Step 1**: Create command file

```bash
# Create file: ram/cli/commands/mycommand.py
```

**Step 2**: Define command

```python
# ram/cli/commands/mycommand.py
import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def run(
    input_text: str = typer.Argument(..., help="Text to process"),
    uppercase: bool = typer.Option(False, "--uppercase", "-u", help="Convert to uppercase")
):
    """
    Process some text.

    This command demonstrates adding a new command to the CLI.
    """
    result = input_text.upper() if uppercase else input_text
    console.print(f"[green]Result:[/green] {result}")
```

**Step 3**: Register in main app

```python
# ram/cli/app.py
from ram.cli.commands import mycommand

# Add this line after app creation:
app.add_typer(mycommand.app, name="mycommand")
```

**Step 4**: Test it

```bash
ram mycommand --help
ram mycommand "hello world"
ram mycommand "hello world" --uppercase
```

---

### Full Example: Command Group

For features with multiple related commands, create a command group.

**Example**: Storage commands (store, retrieve, list)

**Structure**:
```
ram/cli/commands/
└── storage.py      # Command group
```

**Implementation**:
```python
# ram/cli/commands/storage.py
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Memory storage commands")
console = Console()

@app.command()
def store(content: str = typer.Argument(..., help="Content to store")):
    """Store a new memory."""
    # Implementation here
    console.print(f"[green]Stored:[/green] {content}")

@app.command()
def list():
    """List all stored memories."""
    # Implementation here
    table = Table(title="Memories")
    table.add_column("ID", style="cyan")
    table.add_column("Content")
    # Add rows...
    console.print(table)

@app.command()
def delete(memory_id: str = typer.Argument(..., help="Memory ID to delete")):
    """Delete a memory by ID."""
    # Implementation here
    console.print(f"[yellow]Deleted:[/yellow] {memory_id}")
```

**Register**:
```python
# ram/cli/app.py
from ram.cli.commands import storage

app.add_typer(storage.app, name="storage")
```

**Usage**:
```bash
ram storage store "Important information"
ram storage list
ram storage delete abc123
```

---

## Using Rich for Output

The CLI uses Rich library for beautiful terminal output. Here are common patterns:

### Basic Colored Output

```python
from rich.console import Console
console = Console()

# Success (green)
console.print("[green]Success![/green]")

# Error (red)
console.print("[red]Error:[/red] Something went wrong")

# Warning (yellow)
console.print("[yellow]Warning:[/yellow] Be careful")

# Info (blue)
console.print("[blue]Info:[/blue] Processing...")

# Dim/secondary (dim)
console.print("[dim]Additional details...[/dim]")
```

### Tables

```python
from rich.table import Table

table = Table(title="Results")
table.add_column("ID", style="cyan", no_wrap=True)
table.add_column("Name", style="white")
table.add_column("Status", style="green")

table.add_row("1", "Item One", "Active")
table.add_row("2", "Item Two", "Pending")

console.print(table)
```

**Output**:
```
                   Results
┌────┬──────────┬─────────┐
│ ID │ Name     │ Status  │
├────┼──────────┼─────────┤
│ 1  │ Item One │ Active  │
│ 2  │ Item Two │ Pending │
└────┴──────────┴─────────┘
```

### Panels

```python
from rich.panel import Panel

# Success panel
console.print(Panel("[green]Operation completed successfully![/green]", title="Success"))

# Error panel
console.print(Panel(
    "[red]File not found: data.json[/red]\n\nPlease check the file path.",
    title="Error",
    border_style="red"
))
```

### Progress Bars (for long operations)

```python
from rich.progress import track
import time

for item in track(range(100), description="Processing..."):
    time.sleep(0.01)  # Simulate work
```

---

## Typer Patterns

### Arguments vs Options

**Arguments**: Positional, usually required
```python
def command(
    name: str = typer.Argument(..., help="Required name"),
    greeting: str = typer.Argument("Hello", help="Optional greeting")
):
    console.print(f"{greeting}, {name}!")
```

**Options**: Named flags, usually optional
```python
def command(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    output: Path = typer.Option(None, "--output", "-o", help="Output file")
):
    if verbose:
        console.print("[dim]Verbose mode enabled[/dim]")
```

### Type Validation

Typer automatically validates types:

```python
def command(
    count: int = typer.Argument(..., min=1, max=100),  # Must be 1-100
    ratio: float = typer.Option(0.5, min=0.0, max=1.0),  # Must be 0.0-1.0
    output_file: Path = typer.Argument(..., exists=False)  # Must not exist
):
    pass
```

### Custom Validation

```python
def validate_email(email: str) -> str:
    if "@" not in email:
        raise typer.BadParameter("Must be a valid email address")
    return email

def command(
    email: str = typer.Argument(..., callback=validate_email)
):
    console.print(f"Email: {email}")
```

---

## Error Handling

### Standard Pattern

```python
@app.command()
def command(file: Path):
    """Process a file."""
    try:
        # Try to do something
        content = file.read_text()
        console.print("[green]Success![/green]")

    except FileNotFoundError:
        console.print(f"[red]Error:[/red] File not found: {file}")
        console.print("[dim]Hint:[/dim] Check the file path and try again")
        raise typer.Exit(code=1)

    except PermissionError:
        console.print(f"[red]Error:[/red] Permission denied: {file}")
        raise typer.Exit(code=1)

    except Exception as e:
        # Unexpected error - let it crash (prototype approach)
        console.print(f"[red]Unexpected error:[/red] {e}")
        raise
```

### Exit Codes

```python
# Success
raise typer.Exit(code=0)

# General error
raise typer.Exit(code=1)

# Usage error (Typer handles automatically)
raise typer.BadParameter("Invalid value")
```

---

## Testing Your Commands

### Manual Testing Checklist

Per constitution, no automated tests required. Use manual validation:

1. **Help output**:
   ```bash
   ram yourcommand --help
   # Verify: description, arguments, options all shown
   ```

2. **Valid inputs**:
   ```bash
   ram yourcommand valid-input
   # Verify: command succeeds, output is correct
   ```

3. **Invalid inputs**:
   ```bash
   ram yourcommand
   # Verify: error message is clear and helpful
   ```

4. **Exit codes**:
   ```bash
   ram yourcommand valid-input
   echo $?  # Should be 0

   ram yourcommand invalid-input
   echo $?  # Should be 1 or 2
   ```

5. **Output formatting**:
   ```bash
   ram yourcommand
   # Verify: colors render, tables format correctly
   ```

---

## Common Patterns

### Reading from Files

```python
from pathlib import Path

@app.command()
def process(
    input_file: Path = typer.Argument(..., exists=True, readable=True)
):
    """Process a file."""
    try:
        content = input_file.read_text()
        # Process content...
        console.print(f"[green]Processed {input_file}[/green]")
    except Exception as e:
        console.print(f"[red]Error reading file:[/red] {e}")
        raise typer.Exit(code=1)
```

### Writing to Files

```python
@app.command()
def export(
    output_file: Path = typer.Option(None, "--output", "-o")
):
    """Export data to file."""
    data = "Some data to export"

    if output_file:
        output_file.write_text(data)
        console.print(f"[green]Exported to:[/green] {output_file}")
    else:
        console.print(data)  # Print to stdout
```

### Confirmation Prompts

```python
@app.command()
def delete(
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation")
):
    """Delete something dangerous."""
    if not force:
        confirmed = typer.confirm("Are you sure you want to delete this?")
        if not confirmed:
            console.print("[yellow]Cancelled[/yellow]")
            raise typer.Exit(code=0)

    # Proceed with deletion...
    console.print("[green]Deleted![/green]")
```

### Processing Lists

```python
@app.command()
def process_many(
    items: list[str] = typer.Argument(..., help="Items to process")
):
    """Process multiple items."""
    for item in items:
        console.print(f"Processing: {item}")
```

**Usage**: `ram process-many item1 item2 item3`

---

## Project Structure Reference

```
ragged_memory/
├── ram/                        # Main package
│   ├── __init__.py
│   ├── __main__.py            # Entry point
│   ├── version.py             # Version string
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── app.py            # Typer app + global setup
│   │   └── commands/          # Command modules
│   │       ├── __init__.py
│   │       └── demo.py       # Example: hello command
├── pyproject.toml             # Package config
└── README.md
```

**Where to add code**:
- **New command**: Create `ram/cli/commands/yourcommand.py`
- **Register command**: Edit `ram/cli/app.py`
- **Shared utilities**: Create `ram/lib/yourutil.py` (future)
- **Models**: Create `ram/models/yourmodel.py` (future)

---

## Dependencies

Current dependencies in `pyproject.toml`:

```toml
[project]
dependencies = [
    "typer[all]>=0.9.0",  # Includes Rich automatically
]
```

**To add new dependencies**:
1. Add to `pyproject.toml` dependencies list
2. Reinstall: `pip install -e .`

---

## Troubleshooting

### Command not found after install

```bash
# Reinstall in editable mode
pip install -e .

# Or check if entry point is registered
which ram
```

### Rich formatting not working

```bash
# Verify Rich is installed
python -c "import rich; print(rich.__version__)"

# Should show version 13.0+
```

### Import errors

```bash
# Ensure package is installed
pip install -e .

# Check Python version
python --version  # Should be 3.11+
```

### Typer not showing colors

```bash
# Force color output
export FORCE_COLOR=1
ram --help
```

---

## Next Steps

1. **For this feature (001)**: Implement the scaffolding
   - Create package structure
   - Set up Typer app with --version and --help
   - Add demo `hello` command
   - Verify installation and basic usage

2. **For future features**:
   - Feature 002 (storage): Add `store`, `search` commands
   - Feature 003+ (semantic search): Add search implementation
   - Enhance output with more Rich features

3. **Enhancement ideas** (out of scope for prototype):
   - Shell auto-completion
   - Config file support
   - JSON output mode (`--json` flag)
   - Verbose/quiet modes
   - Color theme customization

---

## Summary

**Quick Command Template**:
```python
import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def mycommand(
    arg: str = typer.Argument(..., help="Description"),
    option: bool = typer.Option(False, "--flag", "-f", help="Description")
):
    """Command description for help."""
    try:
        # Your logic here
        console.print("[green]Success![/green]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1)
```

**Remember**:
- All commands need docstrings (for help)
- All parameters need type hints (for validation)
- Use Rich for all output (colors, tables, panels)
- Exit with appropriate codes (0=success, 1=error)
- Let unexpected errors crash (prototype approach)

**Ready to code!** 🚀
