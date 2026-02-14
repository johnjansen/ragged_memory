"""Chunk data model for file indexing."""

from dataclasses import dataclass


@dataclass
class Chunk:
    """Represents a segment of text extracted from a file during chunking.

    Attributes:
        text: The actual text content of the chunk
        start_index: Character position in original file where chunk begins
        end_index: Character position in original file where chunk ends
        chunk_index: Sequential number of this chunk (0-based)
    """

    text: str
    start_index: int
    end_index: int
    chunk_index: int

    @property
    def size(self) -> int:
        """Number of characters in chunk."""
        return len(self.text)
