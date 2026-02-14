"""Storage layer for Ragged Memory - handles local and global memory persistence."""

from ram.storage.scope import StorageScope
from ram.storage.manager import StorageManager

__all__ = ["StorageScope", "StorageManager"]
