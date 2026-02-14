"""File indexing orchestration."""

import hashlib
from datetime import datetime
from pathlib import Path

from ram.indexing.chunker import FileChunker
from ram.indexing.embedder import EmbeddingGenerator
from ram.models.chunk import Chunk


class FileIndexer:
    """Orchestrates the file indexing process: chunk → embed → store.

    Coordinates FileChunker and EmbeddingGenerator to process files and
    prepare them for storage in LanceDB.

    Attributes:
        chunker: FileChunker instance
        embedder: EmbeddingGenerator instance
    """

    def __init__(self):
        """Initialize FileIndexer with default components."""
        self.chunker = FileChunker()
        self.embedder = EmbeddingGenerator()

    def process_file(
        self, file_path: Path, show_progress: bool = False
    ) -> list[dict]:
        """Process a file into index entries ready for storage.

        Args:
            file_path: Path to the file to index
            show_progress: Whether to show progress bars

        Returns:
            List of index entry dicts ready for LanceDB storage
        """
        # Read file content
        content = file_path.read_text(encoding="utf-8")

        # Compute file hash for duplicate detection
        file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

        # Chunk the content
        chunks = self.chunker.chunk(content)

        # Generate embeddings
        embeddings = self.embedder.generate(chunks, show_progress=show_progress)

        # Create index entries
        index_entries = []
        for chunk, embedding in zip(chunks, embeddings):
            entry = {
                "text": chunk.text,
                "vector": embedding.tolist(),
                "file_path": str(file_path.absolute()),
                "chunk_index": chunk.chunk_index,
                "chunk_size": chunk.size,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "file_hash": file_hash,
            }
            index_entries.append(entry)

        return index_entries
