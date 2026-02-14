"""Memory store implementation using LanceDB."""

from pathlib import Path

import lancedb

from ram.storage.scope import StorageScope


class MemoryStore:
    """A persistent collection of memories with a specific scope and storage location.

    Attributes:
        scope: The scope of this store (LOCAL or GLOBAL)
        db_path: Path to the LanceDB database directory
        table_name: Name of the LanceDB table
    """

    def __init__(self, scope: StorageScope, db_path: Path):
        """Initialize a memory store.

        Args:
            scope: StorageScope (LOCAL or GLOBAL)
            db_path: Path where LanceDB files will be stored
        """
        self.scope = scope
        self.db_path = Path(db_path)
        self.table_name = "memories"

    def initialize(self) -> None:
        """Create storage directory and initialize LanceDB connection.

        This creates the directory structure but does not create tables.
        Tables are created on first insert by LanceDB.
        """
        self.db_path.mkdir(parents=True, exist_ok=True)
        # Connect to verify database can be created
        db = lancedb.connect(str(self.db_path))
        # Table will be created on first insert

    def exists(self) -> bool:
        """Check if store directory exists.

        Returns:
            True if the store directory exists, False otherwise
        """
        return self.db_path.exists()

    def get_path(self) -> Path:
        """Get full path to the store.

        Returns:
            Path object pointing to the store directory
        """
        return self.db_path

    def add_chunks(self, chunks: list[dict]) -> None:
        """Add chunk entries to the memory store.

        Args:
            chunks: List of index entry dicts with text, vector, and metadata
        """
        db = lancedb.connect(str(self.db_path))

        # Check if table exists
        try:
            table = db.open_table(self.table_name)
            # Append to existing table
            table.add(chunks)
        except (FileNotFoundError, ValueError):
            # Create new table
            db.create_table(self.table_name, data=chunks)

    def check_file_exists(self, file_hash: str) -> bool:
        """Check if a file with given hash is already indexed.

        Args:
            file_hash: SHA256 hash of file content

        Returns:
            True if file is already indexed, False otherwise
        """
        try:
            db = lancedb.connect(str(self.db_path))
            table = db.open_table(self.table_name)

            # Query for entries with this file hash
            df = table.to_pandas()
            if df.empty:
                return False

            return (df["file_hash"] == file_hash).any()
        except (FileNotFoundError, ValueError):
            # Table doesn't exist yet or other error
            return False
