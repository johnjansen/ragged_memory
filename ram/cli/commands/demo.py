"""Demo command for testing CLI functionality."""

import typer
from rich.console import Console

console = Console()

app = typer.Typer()


@app.command()
def hello(
    name: str = typer.Argument("World", help="Name to greet"),
    uppercase: bool = typer.Option(False, "--uppercase", "-u", help="Convert output to uppercase"),
    count: int = typer.Option(1, "--count", "-c", help="Number of times to greet", min=1, max=10),
):
    """
    Say hello - a demo command with arguments and options.

    This demonstrates argument parsing, validation, and error handling.

    Args:
        name: The name to greet (default: World)
        uppercase: Whether to convert output to uppercase
        count: Number of times to repeat the greeting (1-10)

    Examples:
        $ ram demo hello
        $ ram demo hello Alice
        $ ram demo hello Bob --uppercase
        $ ram demo hello --count 3 Charlie
    """
    try:
        # Validate name is not empty
        if not name or not name.strip():
            console.print("[red]Error:[/red] Name cannot be empty")
            raise typer.Exit(code=1)

        # Create greeting message
        message = f"Hello, {name}!"

        if uppercase:
            message = message.upper()

        # Print greeting 'count' times
        for i in range(count):
            if count > 1:
                console.print(f"[green]{i + 1}.[/green] {message}")
            else:
                console.print(f"[green]{message}[/green]")

        console.print(f"\n[dim]Greeted {name} {count} time(s)[/dim]")

    except ValueError as e:
        console.print(f"[red]Validation error:[/red] {e}")
        raise typer.Exit(code=1)
