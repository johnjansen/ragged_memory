"""Configuration management for Ragged Memory."""

import tomllib
from dataclasses import dataclass
from pathlib import Path

from ram.storage.scope import StorageScope


@dataclass
class Config:
    """Centralized configuration loaded from ~/.ragged_memory/config.toml.

    Attributes:
        embedding_model: Model name for embeddings
        vector_dimensions: Dimension of embedding vectors
        default_scope: Default scope when unspecified
        auto_init_local: Auto-create .ragged_memory/ on first store
        global_dir: Global storage directory
        local_dir: Local storage directory name
    """

    embedding_model: str
    vector_dimensions: int
    default_scope: StorageScope
    auto_init_local: bool
    global_dir: Path
    local_dir: str

    @classmethod
    def load(cls, config_path: Path | None = None) -> "Config":
        """Load config from TOML file, use defaults if missing.

        Args:
            config_path: Path to config.toml file. If None, uses ~/.ragged_memory/config.toml

        Returns:
            Config instance with values from file or defaults
        """
        # Default configuration values
        defaults = {
            "storage": {
                "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
                "vector_dimensions": 384,
            },
            "scope": {
                "default_scope": "local",
                "auto_init_local": True,
            },
            "paths": {
                "global_dir": "~/.ragged_memory",
                "local_dir": ".ragged_memory",
            },
        }

        # Try to load from file, fall back to defaults
        if config_path is None:
            config_path = Path.home() / ".ragged_memory" / "config.toml"

        if config_path.exists():
            with open(config_path, "rb") as f:
                loaded = tomllib.load(f)
                # Merge loaded config with defaults
                for section in defaults:
                    if section in loaded:
                        defaults[section].update(loaded[section])

        # Build Config from merged values
        return cls(
            embedding_model=defaults["storage"]["embedding_model"],
            vector_dimensions=defaults["storage"]["vector_dimensions"],
            default_scope=StorageScope(defaults["scope"]["default_scope"]),
            auto_init_local=defaults["scope"]["auto_init_local"],
            global_dir=Path(defaults["paths"]["global_dir"]).expanduser(),
            local_dir=defaults["paths"]["local_dir"],
        )

    def get_global_dir(self) -> Path:
        """Get the global storage directory path.

        Returns:
            Expanded path to global directory
        """
        return self.global_dir.expanduser()
