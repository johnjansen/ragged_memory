"""Main CLI application using Typer and Rich."""

import typer
from rich.console import Console

from ram.version import __version__
from ram.cli.commands import demo

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
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    )
):
    """
    Ragged Memory (RAM) - Semantic memory for LLMs.

    A lightweight CLI tool for storing and retrieving information
    with semantic search capabilities.
    """
    pass


# Register command modules
app.add_typer(demo.app, name="demo")
