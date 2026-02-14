"""Storage scope enumeration for Ragged Memory."""

from enum import Enum


class StorageScope(Enum):
    """Defines the visibility boundary for stored memories.

    LOCAL: Project-local scope (stored in .ragged_memory/ within project)
    GLOBAL: User-global scope (stored in ~/.ragged_memory/ in user home)
    """

    LOCAL = "local"
    GLOBAL = "global"
