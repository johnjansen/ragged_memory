"""Storage manager for coordinating local and global memory stores."""

from pathlib import Path

from ram.storage.config import Config
from ram.storage.context import ProjectContext
from ram.storage.scope import StorageScope
from ram.storage.store import MemoryStore


class StorageManager:
    """Manages access to local and global memory stores.

    Attributes:
        config: Configuration settings
        context: Project context for local store detection
    """

    def __init__(self, config: Config | None = None, context: ProjectContext | None = None):
        """Initialize storage manager.

        Args:
            config: Configuration instance. If None, loads default config.
            context: Project context. If None, detects from current directory.
        """
        self.config = config if config is not None else Config.load()
        self.context = context if context is not None else ProjectContext()

    def get_store(self, scope: StorageScope | None = None) -> MemoryStore:
        """Get a memory store for the specified scope.

        Args:
            scope: StorageScope (LOCAL or GLOBAL). If None, uses default from config.

        Returns:
            MemoryStore instance for the requested scope

        Raises:
            ValueError: If LOCAL scope requested but no project detected
        """
        if scope is None:
            scope = self.config.default_scope

        if scope == StorageScope.LOCAL:
            if self.context.project_root is None:
                raise ValueError(
                    "No project detected. Run 'ram init' to create a local store."
                )
            store_path = self.context.store_path
        else:  # GLOBAL
            store_path = self.config.get_global_dir()

        store = MemoryStore(scope, store_path)

        # Auto-initialize global store if it doesn't exist
        if scope == StorageScope.GLOBAL and not store.exists():
            self._initialize_global_store(store)

        return store

    def _initialize_global_store(self, store: MemoryStore) -> None:
        """Initialize global store with default configuration.

        Args:
            store: MemoryStore instance for global scope
        """
        # Create global directory
        store.initialize()

        # Create default config.toml if it doesn't exist
        config_path = store.get_path() / "config.toml"
        if not config_path.exists():
            default_config = """[storage]
embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
vector_dimensions = 384

[scope]
default_scope = "local"
auto_init_local = true

[paths]
global_dir = "~/.ragged_memory"
local_dir = ".ragged_memory"
"""
            config_path.write_text(default_config)
