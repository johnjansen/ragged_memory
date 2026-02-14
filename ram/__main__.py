"""Entry point for RAM CLI - enables `python -m ram` and `ram` command."""

from ram.cli.app import app


def main():
    """Main entry point for the CLI application."""
    app()


if __name__ == "__main__":
    main()
