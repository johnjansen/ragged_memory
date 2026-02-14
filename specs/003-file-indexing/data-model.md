# Data Model: File Indexing and Embedding

**Feature**: 003-file-indexing
**Date**: 2026-02-14

## Entities

### Chunk (Dataclass)

Represents a segment of text extracted from a file during chunking.

**Attributes**:
- `text` (str): The actual text content of the chunk
- `start_index` (int): Character position in original file where chunk begins
- `end_index` (int): Character position in original file where chunk ends
- `chunk_index` (int): Sequential number of this chunk (0-based)

**Usage**:
```python
from dataclasses import dataclass

@dataclass
class Chunk:
    text: str
    start_index: int
    end_index: int
    chunk_index: int

    @property
    def size(self) -> int:
        """Number of characters in chunk."""
        return len(self.text)
```

**Lifecycle**:
1. Created by `FileChunker` when processing source file
2. Passed to `EmbeddingGenerator` for vector generation
3. Combined with embedding and metadata to create `IndexEntry`
4. Discarded after storage (data persisted in LanceDB)

---

### IndexEntry (Dict)

A record stored in LanceDB containing chunk text, embedding, and metadata.

**Schema** (LanceDB table format):
```python
{
    "text": str,           # Chunk text content (searchable)
    "vector": list[float], # 384-dim embedding from sentence-transformers
    "file_path": str,      # Absolute path to source file
    "chunk_index": int,    # Position in file (0, 1, 2, ...)
    "chunk_size": int,     # Character count in chunk
    "timestamp": str,      # ISO 8601 timestamp (e.g., "2026-02-14T10:30:00Z")
    "file_hash": str,      # SHA256 hex digest of source file content
}
```

**Creation**:
```python
import hashlib
from datetime import datetime

def create_index_entry(
    chunk: Chunk,
    embedding: list[float],
    file_path: Path,
    file_content: str
) -> dict:
    """Create index entry from chunk and embedding."""
    file_hash = hashlib.sha256(file_content.encode('utf-8')).hexdigest()

    return {
        "text": chunk.text,
        "vector": embedding.tolist(),
        "file_path": str(file_path.absolute()),
        "chunk_index": chunk.chunk_index,
        "chunk_size": chunk.size,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "file_hash": file_hash,
    }
```

**Storage**:
```python
# Append to LanceDB table
table = db.open_table("memories")
table.add(index_entries)  # List of dicts
```

**Retrieval**:
```python
# Search by vector similarity
results = table.search(query_vector).limit(10).to_pandas()

# Filter by file
results = table.search(query_vector) \
    .where("file_path = '/path/to/file'") \
    .to_pandas()

# Result columns: text, vector, file_path, chunk_index, etc.
```

---

### FileMetadata (Computed)

Information about a source file derived during indexing. Not stored as separate entity - captured in IndexEntry records.

**Attributes**:
- `path` (Path): Absolute filesystem path
- `size_bytes` (int): File size in bytes
- `hash` (str): SHA256 hash of content (for duplicate detection)
- `encoding` (str): Always "utf-8" (per requirements)
- `chunk_count` (int): Number of chunks created from this file

**Computation**:
```python
from pathlib import Path
import hashlib

class FileMetadata:
    def __init__(self, file_path: Path):
        self.path = file_path.absolute()
        self.content = self.path.read_text(encoding='utf-8')
        self.size_bytes = len(self.content.encode('utf-8'))
        self.hash = hashlib.sha256(self.content.encode('utf-8')).hexdigest()
        self.encoding = "utf-8"
        self.chunk_count = 0  # Set after chunking
```

**Usage**:
- Validate file before processing
- Detect duplicates (check if hash exists in LanceDB)
- Provide user feedback on indexing progress

---

## Relationships

```
File (on disk)
    ↓ read_text()
FileContent (string)
    ↓ FileChunker.chunk()
List[Chunk]
    ↓ EmbeddingGenerator.embed()
List[Chunk] + List[Embedding]
    ↓ create_index_entries()
List[IndexEntry]
    ↓ LanceDB.add()
Stored in "memories" table
```

---

## Data Flow

```
User runs: ram add document.txt

1. Read file:
   - Validate UTF-8 encoding
   - Compute file hash
   - Load content into memory

2. Chunk text:
   - Initialize Chonkie SemanticChunker
   - Split content into List[Chunk]
   - Each chunk knows its position in source

3. Generate embeddings:
   - Load sentence-transformers model
   - Encode all chunks → numpy array (n_chunks, 384)

4. Create index entries:
   - Combine chunks + embeddings + metadata
   - Build List[IndexEntry] dicts

5. Store in LanceDB:
   - Determine scope (local or global)
   - Append entries to appropriate table
   - Confirm success to user
```

---

## Storage Layout

### LanceDB Table Structure

```
.ragged_memory/memories.lance/         # Local scope
└── [LanceDB internal files]

~/.ragged_memory/memories.lance/       # Global scope
└── [LanceDB internal files]
```

**Table name**: `memories` (shared for all content - simple files, chunks from files, etc.)

**Index strategy**: LanceDB automatically creates vector index for similarity search

**Query patterns**:
```python
# Semantic search (similarity)
results = table.search(query_embedding).limit(10)

# Filter by file
results = table.search(query_embedding) \
    .where(f"file_path = '{file_path}'") \
    .limit(10)

# Get all chunks from a file (ordered)
results = table.to_pandas()
results = results[results['file_path'] == file_path]
results = results.sort_values('chunk_index')
```

---

## Validation Rules

1. **File must be UTF-8 encoded**:
   - Attempt to read as UTF-8
   - Raise clear error if UnicodeDecodeError occurs

2. **File must not exceed 10MB**:
   - Check file size after loading
   - Raise error if too large

3. **File path must be readable**:
   - Check file exists and has read permissions
   - Raise FileNotFoundError or PermissionError

4. **Chunks must have non-empty text**:
   - Filter out empty chunks after Chonkie processing
   - Skip chunks with only whitespace

5. **Embeddings must match chunk count**:
   - Verify len(embeddings) == len(chunks)
   - Fail if mismatch (indicates processing error)

---

## State Transitions

### Indexing Process

```
FILE_DISCOVERED → (validate) → FILE_VALID
    ↓
FILE_VALID → (read) → CONTENT_LOADED
    ↓
CONTENT_LOADED → (chunk) → CHUNKS_CREATED
    ↓
CHUNKS_CREATED → (embed) → EMBEDDINGS_GENERATED
    ↓
EMBEDDINGS_GENERATED → (store) → INDEXED
```

### Error States

```
FILE_DISCOVERED → (validate) → ERROR_NOT_FOUND
FILE_DISCOVERED → (validate) → ERROR_NOT_UTF8
FILE_VALID → (read) → ERROR_TOO_LARGE
CONTENT_LOADED → (chunk) → ERROR_NO_CHUNKS
CHUNKS_CREATED → (embed) → ERROR_EMBEDDING_FAILED
EMBEDDINGS_GENERATED → (store) → ERROR_STORAGE_FAILED
```

---

## Example Record

```python
{
    "text": "Ragged Memory (RAM) is a CLI tool that gives LLMs...",
    "vector": [0.023, -0.145, 0.089, ..., 0.234],  # 384 floats
    "file_path": "/Users/john/projects/ragged_memory/README.md",
    "chunk_index": 0,
    "chunk_size": 512,
    "timestamp": "2026-02-14T15:30:45Z",
    "file_hash": "a3f5c9d2e1b4..."  # SHA256 hex
}
```

**Interpretation**:
- This is the first chunk (index 0) from README.md
- Contains 512 characters of text
- Indexed on 2026-02-14 at 15:30:45 UTC
- Can be found via similarity search on the 384-dim vector
- Can be filtered to show only chunks from this specific file
- File hash allows duplicate detection across indexing runs
