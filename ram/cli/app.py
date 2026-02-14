"""Main CLI application using Typer and Rich."""

import typer
from rich.console import Console

from ram.version import __version__
from ram.cli.commands import demo, init, add
from ram.cli.common import get_active_scope

# Create Typer app instance
app = typer.Typer(
    name="ram",
    help="Ragged Memory - Semantic memory for LLMs at the command line",
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="rich",
)

# Create Rich console for formatted output
console = Console()


def version_callback(value: bool):
    """Display version information and exit."""
    if value:
        console.print(f"[cyan]Ragged Memory (RAM)[/cyan] version [bold]{__version__}[/bold]")
        raise typer.Exit()


@app.callback()
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    ),
    global_scope: bool = typer.Option(
        False,
        "--global",
        "-g",
        help="Use global memory store (user-wide)",
    ),
    local_scope: bool = typer.Option(
        False,
        "--local",
        "-l",
        help="Use local memory store (project-specific)",
    ),
):
    """
    Ragged Memory (RAM) - Semantic memory for LLMs.

    A lightweight CLI tool for storing and retrieving information
    with semantic search capabilities.
    """
    # Validate scope flags (mutually exclusive)
    if global_scope and local_scope:
        console.print("[red]Error:[/red] Cannot specify both --global and --local flags")
        raise typer.Exit(1)

    # Store scope flags in context for commands to access
    ctx.obj = {
        "global_flag": global_scope,
        "local_flag": local_scope,
    }

    try:
        # Determine active scope (this will validate flags and context)
        active_scope = get_active_scope(global_scope, local_scope)
        ctx.obj["active_scope"] = active_scope
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


# Register command modules
app.add_typer(demo.app, name="demo")
app.command(name="init", help="Initialize a project-local memory store")(init.init)
app.command(name="add", help="Index a text file into memory store")(add.add)
