# Feature Specification: File Indexing and Embedding

**Feature Branch**: `003-file-indexing`
**Created**: 2026-02-14
**Status**: Draft
**Input**: User description: "ram add file_path should read, chunk, embed and index the file into lancedb, locally or globally depending on the presence of the --global arg"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Basic File Indexing (Priority: P1)

Users need to add files to their memory store so that the content becomes searchable. This allows developers to index documentation, code files, notes, or any text content into RAM for later semantic retrieval.

**Why this priority**: This is the core value proposition - without the ability to index files, the memory store remains empty and unusable. This is the MVP that makes RAM functional.

**Independent Test**: Can be fully tested by running `ram add <file>` with a text file, verifying the file is read and indexed, and confirming the content is retrievable through search.

**Acceptance Scenarios**:

1. **Given** a user has initialized a local store, **When** they run `ram add document.txt`, **Then** the file content is indexed into the local store
2. **Given** a user provides a valid file path, **When** the file is indexed, **Then** they receive confirmation showing the file was successfully added
3. **Given** a file has been indexed, **When** the user searches for content from that file, **Then** the search returns relevant results from the indexed content
4. **Given** a user provides an invalid file path, **When** they attempt to index it, **Then** they receive a clear error message indicating the file was not found

---

### User Story 2 - Intelligent Chunking (Priority: P2)

Users need to index large files without hitting memory or embedding limits. The system should automatically split large files into manageable chunks while preserving context and meaning.

**Why this priority**: Large documentation files, codebases, or books cannot be processed as single units due to embedding model token limits. Chunking enables RAM to handle real-world content sizes.

**Independent Test**: Can be tested by indexing a large file (>10KB) and verifying it's split into multiple chunks, each chunk is embedded separately, and search results span chunks correctly.

**Acceptance Scenarios**:

1. **Given** a user indexes a large file, **When** the file exceeds the chunk size threshold, **Then** it is automatically split into smaller chunks
2. **Given** a file is chunked, **When** content spans multiple chunks, **Then** search can still find relevant information across chunk boundaries
3. **Given** a file with natural section boundaries (paragraphs, code functions), **When** chunking occurs, **Then** splits happen at semantic boundaries when possible
4. **Given** multiple chunks from the same file, **When** displaying search results, **Then** the system indicates which file and chunk the result came from

---

### User Story 3 - Scope-Aware Indexing (Priority: P3)

Users need to control whether files are indexed into project-local or user-global storage. Some files (like project documentation) belong in local scope, while others (like personal reference materials) belong in global scope.

**Why this priority**: Scope control ensures proper isolation - project-specific files don't pollute global storage, and personal knowledge bases remain accessible across projects. This builds on existing scope infrastructure.

**Independent Test**: Can be tested by indexing a file with `--global` flag, navigating to different directories, and verifying the indexed content is accessible globally but not appearing in local-only searches.

**Acceptance Scenarios**:

1. **Given** a user runs `ram add document.txt` without flags, **When** inside a project directory, **Then** the file is indexed to local storage
2. **Given** a user runs `ram --global add document.txt`, **When** executed from any directory, **Then** the file is indexed to global storage
3. **Given** a file is indexed locally, **When** the user switches to a different project, **Then** that file's content is not visible in the new project's searches
4. **Given** a file is indexed globally, **When** the user searches from any directory, **Then** the global file content is accessible

---

### Edge Cases

- What happens when a user attempts to index a binary file (PDF, image, etc.)?
- How does the system handle files with non-UTF-8 encoding?
- What happens when a file is too large even after chunking?
- How does the system handle files that are deleted or moved after indexing?
- What happens if the same file is added multiple times?
- How does the system handle symbolic links or relative paths?
- What happens when attempting to index a file without read permissions?
- How does chunking handle files with no clear structure (single long paragraph)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept a file path as input and read the file contents
- **FR-002**: System MUST validate the file exists and is readable before processing
- **FR-003**: System MUST support both absolute and relative file paths
- **FR-004**: System MUST chunk files that exceed a maximum size threshold
- **FR-005**: System MUST generate embeddings for each chunk using the configured embedding model
- **FR-006**: System MUST store chunks and their embeddings in the appropriate LanceDB store (local or global)
- **FR-007**: System MUST respect the --global and --local flags for scope selection
- **FR-008**: System MUST provide feedback on indexing progress and completion
- **FR-009**: System MUST handle common error cases (file not found, permission denied, invalid encoding)
- **FR-010**: System MUST associate indexed chunks with their source file path and metadata
- **FR-011**: System MUST prevent duplicate indexing of the same file content
- **FR-012**: System MUST handle text files with common encodings (UTF-8, ASCII, Latin-1)

### Key Entities

- **File**: A document on disk to be indexed. Has a path, content, size, and encoding. The system reads and processes this content.
- **Chunk**: A segment of file content sized appropriately for embedding. Has text content, position in original file, and metadata linking back to source file.
- **Embedding**: A vector representation of a chunk's semantic meaning. Generated by embedding model and stored alongside the chunk for similarity search.
- **Index Entry**: A record in LanceDB containing the chunk text, its embedding vector, and metadata (file path, chunk position, timestamp, scope).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can index a text file in under 5 seconds for files up to 100KB
- **SC-002**: Indexed file content is findable through semantic search with 95% relevance accuracy
- **SC-003**: Chunking preserves context such that search results remain coherent and useful
- **SC-004**: Users receive clear feedback on indexing status within 1 second of command execution
- **SC-005**: The system handles at least 10 file types (txt, md, py, js, java, etc.) without errors
- **SC-006**: Zero data loss occurs during chunking and embedding process
- **SC-007**: Scope selection (--global vs default) correctly isolates indexed content 100% of the time

### Assumptions

- Users primarily want to index text-based files (code, documentation, notes)
- The embedding model from configuration (sentence-transformers/all-MiniLM-L6-v2) is suitable for general text
- Chunk size of 512-1024 tokens balances context preservation with embedding limits
- Users prefer automatic chunking over manual control
- File paths are provided by users who have filesystem access and permissions
- Files remain static after indexing (updates/deletions handled in future features)
- UTF-8 is the primary encoding, with fallback support for common alternatives

### Dependencies

- **002-storage-scopes**: Requires local and global storage infrastructure
- **Embedding model**: Requires sentence-transformers library and model loading
- **File I/O**: Requires Python pathlib and encoding detection

### Scope

**In Scope**:
- Indexing single files via command line
- Automatic chunking for large files
- Text file processing (multiple encodings)
- Embedding generation and storage
- Scope selection (--global/--local)
- Basic error handling and user feedback
- Metadata tracking (file path, timestamp, chunk position)

**Out of Scope**:
- Batch indexing of multiple files or directories (future)
- Binary file handling (PDF, DOCX parsing) (future)
- Incremental updates when files change (future)
- Deduplication across multiple file versions (future)
- Custom chunking strategies (future)
- Progress bars for large file processing (future)
- File watching/auto-indexing (future)
- Removing or updating indexed files (future)
