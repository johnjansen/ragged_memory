"""Add command for indexing files into memory store."""

from pathlib import Path

import typer
from rich.console import Console

from ram.indexing.indexer import FileIndexer
from ram.storage.manager import StorageManager
from ram.storage.scope import StorageScope

console = Console()


def add(ctx: typer.Context, file_path: str) -> None:
    """Index a text file into memory store for semantic search.

    Reads a UTF-8 text file, chunks it intelligently, generates embeddings,
    and stores chunks in LanceDB (local or global scope).

    Args:
        ctx: Typer context with scope flags from parent
        file_path: Path to the file to index
    """
    # Convert to Path object
    path = Path(file_path)

    # Validate file exists
    if not path.exists():
        console.print(f"[red]✗[/red] Error: File '{file_path}' not found")
        console.print("\nCheck the file path and try again.")
        raise typer.Exit(1)

    # Validate file is readable
    if not path.is_file():
        console.print(f"[red]✗[/red] Error: '{file_path}' is not a file")
        raise typer.Exit(1)

    # Try to read as UTF-8
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        console.print(
            f"[red]✗[/red] Error: File '{file_path}' is not UTF-8 encoded"
        )
        console.print(
            "\nThis command only supports text files. Convert to UTF-8 or use a different tool."
        )
        raise typer.Exit(1)
    except PermissionError:
        console.print(
            f"[red]✗[/red] Error: Permission denied reading '{path.absolute()}'"
        )
        console.print("\nCheck file permissions and try again.")
        raise typer.Exit(1)

    # Check file size (10MB limit)
    file_size_mb = len(content.encode("utf-8")) / 1024 / 1024
    if file_size_mb > 10:
        console.print(
            f"[red]✗[/red] Error: File '{file_path}' is too large ({file_size_mb:.1f} MB)"
        )
        console.print("\nMaximum file size: 10 MB. Split the file or remove content.")
        raise typer.Exit(1)

    # Determine scope from context
    storage_manager = StorageManager()

    # Get scope flags from parent context
    global_flag = ctx.obj.get("global_flag", False) if ctx.obj else False
    local_flag = ctx.obj.get("local_flag", False) if ctx.obj else False

    # Determine active scope
    if global_flag:
        scope = StorageScope.GLOBAL
    elif local_flag:
        scope = StorageScope.LOCAL
    else:
        # Use default scope detection
        scope = storage_manager.config.default_scope
        if storage_manager.context.project_root:
            scope = StorageScope.LOCAL

    # Get appropriate store
    try:
        store = storage_manager.get_store(scope)
    except ValueError as e:
        console.print(f"[red]✗[/red] Error: {e}")
        raise typer.Exit(1)

    # Check for duplicates
    import hashlib

    file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

    if store.check_file_exists(file_hash):
        console.print(f"File already indexed (hash: {file_hash[:12]}...)")
        console.print(f"Previously indexed")
        console.print()

        # Ask user if they want to re-index
        response = typer.confirm("Re-index? This will add duplicate chunks.")
        if not response:
            console.print("Skipped indexing.")
            raise typer.Exit(0)

    # Show progress for large files
    show_progress = file_size_mb > 1.0

    # Process file
    console.print(f"Chunking... ", end="")
    indexer = FileIndexer()

    try:
        index_entries = indexer.process_file(path, show_progress=show_progress)
    except Exception as e:
        console.print(f"\n[red]✗[/red] Error during processing: {e}")
        raise typer.Exit(1)

    chunk_count = len(index_entries)
    console.print(f"{chunk_count} chunks created")

    if show_progress:
        console.print("Generating embeddings...")

    # Store chunks
    console.print("Storing chunks... ", end="")

    try:
        store.add_chunks(index_entries)
        console.print("done")
    except Exception as e:
        console.print(f"\n[red]✗[/red] Error storing chunks: {e}")
        raise typer.Exit(1)

    # Success message
    console.print(
        f"[green]✓[/green] Indexed {chunk_count} chunks from {path.name}"
    )
    console.print()

    # Show scope indicator
    scope_name = "global" if scope == StorageScope.GLOBAL else f"local: {path.parent.name}"
    console.print(f"[{'magenta' if scope == StorageScope.GLOBAL else 'cyan'}][{scope_name}][/] {chunk_count} chunks")
    console.print()

    console.print("Next: Search with 'ram search \"query text\"'")
