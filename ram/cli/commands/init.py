"""Initialize command for creating project-local memory stores."""

from pathlib import Path

import typer
from rich.console import Console

from ram.storage.config import Config
from ram.storage.context import ProjectContext
from ram.storage.scope import StorageScope
from ram.storage.store import MemoryStore

console = Console()


def init(ctx: typer.Context) -> None:
    """Initialize a project-local memory store in the current directory.

    Creates a .ragged_memory/ directory in the current working directory
    and initializes a LanceDB database for storing project-specific memories.

    This command is idempotent - running it multiple times is safe.

    Note: This command always creates a LOCAL store. The --global flag is not
    applicable since global stores are auto-initialized on first use.
    """
    # Check if --global flag was used (invalid for init)
    if ctx.obj and ctx.obj.get("global_flag"):
        console.print(
            "[yellow]Note:[/yellow] Global store is auto-initialized on first use."
        )
        console.print("The --global flag is not needed with 'ram init'.")
        console.print(
            "\nTo use global storage, simply omit 'ram init' and use other commands with --global."
        )
        raise typer.Exit(0)

    # Get current directory
    current_dir = Path.cwd()
    store_dir = current_dir / ".ragged_memory"

    # Check if already initialized
    if store_dir.exists():
        console.print(
            f"[green]✓[/green] Local store already initialized at {store_dir.relative_to(current_dir)}"
        )
        console.print("\nUse 'ram store' to add memories to this project.")
        raise typer.Exit(0)

    # Create and initialize the store
    try:
        store = MemoryStore(StorageScope.LOCAL, store_dir)
        store.initialize()

        console.print(f"[green]✓[/green] Created {store_dir.relative_to(current_dir)}")
        console.print("[green]✓[/green] Initialized local memory store")
        console.print("[green]✓[/green] Project ready for local memories")

        console.print("\n[bold]Next steps:[/bold]")
        console.print('  ram store "your memory text"          # Store a memory locally')
        console.print('  ram search "query"                    # Search local memories')
        console.print(
            '  ram store --global "your memory"      # Store globally instead'
        )

    except PermissionError:
        console.print(
            f"[red]✗[/red] Error: Permission denied creating {store_dir.relative_to(current_dir)}"
        )
        console.print("\nCheck directory permissions and try again.")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise typer.Exit(1)
