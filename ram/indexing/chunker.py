"""File chunking using Chonkie's SemanticChunker."""

from chonkie import SemanticChunker

from ram.models.chunk import Chunk


class FileChunker:
    """Chunks text files using semantic boundaries.

    Uses Chonkie's SemanticChunker for intelligent content-aware splitting
    that respects paragraph and sentence boundaries.

    Attributes:
        chunker: Chonkie SemanticChunker instance
    """

    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        """Initialize FileChunker.

        Args:
            chunk_size: Target size in tokens per chunk (default: 512)
            chunk_overlap: Overlap in tokens between chunks (default: 50)
        """
        self.chunker = SemanticChunker(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def chunk(self, text: str) -> list[Chunk]:
        """Chunk text into semantic segments.

        Args:
            text: Text content to chunk

        Returns:
            List of Chunk objects with text and position information
        """
        # Use Chonkie to split text
        chonkie_chunks = self.chunker.chunk(text)

        # Convert to our Chunk model
        chunks = []
        for idx, chonkie_chunk in enumerate(chonkie_chunks):
            chunk = Chunk(
                text=chonkie_chunk.text,
                start_index=chonkie_chunk.start_index,
                end_index=chonkie_chunk.start_index + len(chonkie_chunk.text),
                chunk_index=idx,
            )
            chunks.append(chunk)

        return chunks
