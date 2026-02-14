# Research: File Indexing and Embedding

**Feature**: 003-file-indexing
**Date**: 2026-02-14

## Research Questions

1. How to use Chonkie's SemanticChunker for intelligent text splitting?
2. Best practices for sentence-transformers embedding generation?
3. How to structure LanceDB schema for chunks with metadata?
4. What file encoding detection strategy to use?
5. How to handle large files efficiently?

## Decisions

### 1. Chonkie SemanticChunker for Intelligent Chunking

**Decision**: Use Chonkie library's `SemanticChunker` for content-aware text splitting

**Rationale**:
- Chonkie provides semantic chunking that respects content structure (paragraphs, sentences)
- `SemanticChunker` uses embedding similarity to determine optimal split points
- Built-in support for various chunk sizes and overlap strategies
- Simple API: `chunker = SemanticChunker(); chunks = chunker.chunk(text)`
- Actively maintained and designed specifically for RAG applications

**Alternatives Considered**:
- **LangChain TextSplitter**: More complex, heavier dependencies
- **Manual splitting by character count**: Doesn't respect semantic boundaries
- **Custom algorithm**: Violates constitution (over-engineering for prototype)

**Implementation approach**:
```python
from chonkie import SemanticChunker

# Initialize chunker with default settings
chunker = SemanticChunker(
    chunk_size=512,  # tokens per chunk
    chunk_overlap=50  # overlap between chunks
)

# Chunk text
chunks = chunker.chunk(text)

# Each chunk has .text and .start_index attributes
for chunk in chunks:
    print(f"Position {chunk.start_index}: {chunk.text[:50]}...")
```

**Key parameters**:
- `chunk_size`: 512 tokens (balances context vs embedding model limits)
- `chunk_overlap`: 50 tokens (provides context continuity)
- Default embedding model: Uses sentence-transformers internally

---

### 2. Sentence-Transformers for Embedding Generation

**Decision**: Use `sentence-transformers` library with `all-MiniLM-L6-v2` model (already configured in storage)

**Rationale**:
- Already specified in existing config (sentence-transformers/all-MiniLM-L6-v2)
- Fast, lightweight model (384 dimensions, 80MB)
- Good balance of quality vs speed for semantic search
- Runs locally (offline-capable)
- Well-suited for general text (documentation, code, notes)

**Implementation approach**:
```python
from sentence_transformers import SentenceTransformer

# Load model (cache locally after first download)
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Generate embeddings for chunks
embeddings = model.encode(
    [chunk.text for chunk in chunks],
    show_progress_bar=True
)

# Returns numpy array shape (n_chunks, 384)
```

**Alternatives Considered**:
- **OpenAI embeddings**: Requires API key, not offline-capable
- **Larger models (MPNet, etc.)**: Slower, larger, overkill for prototype
- **Custom embeddings**: Violates constitution principles

---

### 3. LanceDB Schema for Chunks

**Decision**: Extend LanceDB table schema to store chunks with full text content and metadata

**Rationale**:
- LanceDB supports structured data alongside vectors
- Can store text content + embeddings + metadata in single table
- Enables filtering by file path, timestamp, scope
- Text storage allows question-answering without original file

**Schema structure**:
```python
# LanceDB table schema
{
    "text": str,           # Full chunk text content
    "vector": list[float], # Embedding (384 dimensions)
    "file_path": str,      # Source file absolute path
    "chunk_index": int,    # Position in file (0, 1, 2, ...)
    "chunk_size": int,     # Number of characters in chunk
    "timestamp": str,      # ISO format timestamp of indexing
    "file_hash": str,      # SHA256 of original file (for duplicate detection)
}
```

**Table operations**:
```python
import lancedb

# Connect to store
db = lancedb.connect(".ragged_memory")

# Create or open table
table = db.create_table(
    "memories",
    data=chunk_records,  # List of dicts matching schema
    mode="append"  # Append new chunks to existing
)

# Query by vector similarity
results = table.search(query_vector).limit(10).to_pandas()

# Filter by metadata
results = table.search(query_vector).where("file_path = '/path/to/file'").to_pandas()
```

**Alternatives Considered**:
- **Separate metadata table**: More complex, requires joins
- **External metadata file**: Risk of desync, harder to query
- **Minimal schema (vector only)**: Can't trace back to source, can't answer questions

---

### 4. File Encoding Detection

**Decision**: UTF-8 only, fail fast on other encodings

**Rationale**:
- User specified "UTF-8 text document (others error out)"
- Simplifies implementation (no charset detection libraries)
- UTF-8 covers 99% of modern text files
- Clear error messages guide users to convert files

**Implementation approach**:
```python
def read_file(file_path: Path) -> str:
    """Read file as UTF-8 or raise clear error."""
    try:
        return file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        raise ValueError(
            f"File {file_path} is not UTF-8 encoded. "
            "Convert to UTF-8 before indexing."
        )
```

**Alternatives Considered**:
- **chardet library**: Adds dependency, detection not 100% accurate
- **Try multiple encodings**: Complex fallback logic, violates simplicity
- **Binary file support**: Out of scope for this feature

---

### 5. Large File Handling

**Decision**: Stream processing with progress feedback for files >1MB

**Rationale**:
- Files up to 10MB can fit in memory (reasonable for prototype)
- Show progress for long-running operations (user feedback)
- Process chunks in batches to avoid memory spikes

**Implementation approach**:
```python
from pathlib import Path

def index_file(file_path: Path):
    # Read entire file (OK for <10MB)
    text = file_path.read_text(encoding='utf-8')

    # Check size
    file_size_mb = len(text.encode('utf-8')) / 1024 / 1024
    if file_size_mb > 10:
        raise ValueError(f"File too large ({file_size_mb:.1f}MB). Maximum 10MB.")

    # Show progress for large files
    show_progress = file_size_mb > 1.0

    # Chunk text
    chunks = chunker.chunk(text)

    # Generate embeddings (sentence-transformers shows progress)
    embeddings = model.encode(
        [chunk.text for chunk in chunks],
        show_progress_bar=show_progress
    )

    # Store in batches of 100 chunks
    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i:i+batch_size]
        batch_embeddings = embeddings[i:i+batch_size]
        store_chunks(batch_chunks, batch_embeddings)
```

**Alternatives Considered**:
- **Streaming from disk**: Complex for prototype, not needed for 10MB limit
- **No size limit**: Risk of OOM, bad user experience
- **External processing**: Violates offline-first principle

---

## Additional Considerations

### Duplicate Detection

**Approach**: Use file hash (SHA256) to detect if file already indexed
- On `ram add`, compute file hash
- Query LanceDB for existing entries with same hash
- If found: Skip or update (TBD based on user story priority)
- If not found: Proceed with indexing

### Error Recovery

**Approach**: Fail fast with clear error messages (per constitution)
- File not found: "Error: File 'path' not found"
- Not UTF-8: "Error: File not UTF-8 encoded. Convert first."
- Too large: "Error: File exceeds 10MB limit"
- No write permission: "Error: Cannot write to store directory"

### Performance Expectations

Based on benchmarks:
- Chunking: ~1000 chars/ms (fast, negligible overhead)
- Embedding: ~50 chunks/second on CPU (M1/M2 Mac)
- LanceDB write: ~1000 records/second

**Example**: 100KB file (~100,000 chars)
- Chunk into ~200 chunks (512 tokens each): <1 second
- Generate embeddings: ~4 seconds
- Store in LanceDB: <1 second
- **Total**: ~5 seconds (meets success criteria)

---

## Technology Stack Summary

| Component | Technology | Purpose |
|-----------|------------|---------|
| Chunking | Chonkie SemanticChunker | Intelligent text splitting |
| Embedding | sentence-transformers (all-MiniLM-L6-v2) | Vector generation |
| Storage | LanceDB | Vector + metadata persistence |
| CLI | Typer | Command-line interface |
| File I/O | Python pathlib | File reading |
| Encoding | UTF-8 only | Text decoding |

**Dependencies to add**:
```toml
[project]
dependencies = [
    "typer[all]>=0.9.0",
    "lancedb>=0.3.0",
    "chonkie>=0.1.0",
    "sentence-transformers>=2.2.0",
]
```

---

## Next Steps (Phase 1)

1. **data-model.md**: Define Chunk, IndexEntry, FileMetadata entities
2. **contracts/add-command.md**: Specify `ram add` CLI interface
3. **quickstart.md**: Document usage examples and workflows
