# CLI Contract: ram add

**Command**: `ram add <file>`
**Purpose**: Index a text file into memory store for semantic search

## Signature

```bash
ram [--global|-g] [--local|-l] add <FILE>
```

**Note**: Scope flags (`--global`, `--local`) are defined at the parent level (`ram`), not on the `add` subcommand.

## Arguments

### FILE (required)

Path to the text file to index.

- **Type**: Path (string)
- **Format**: Relative or absolute file path
- **Validation**:
  - Must exist and be readable
  - Must be UTF-8 encoded text file
  - Must not exceed 10MB in size
- **Examples**:
  - `document.txt` (relative path)
  - `/Users/john/notes/ideas.md` (absolute path)
  - `../shared/README.md` (relative with parent directory)

## Options

None - the command accepts only the file path argument. Scope selection is handled by parent-level flags.

## Behavior

### 1. Validate Input

- Check file exists
  - If not: Error and exit with code 1
- Check file is readable
  - If not: PermissionError and exit with code 1
- Attempt to read as UTF-8
  - If fails: UnicodeDecodeError with conversion guidance, exit with code 1
- Check file size
  - If > 10MB: Error with size information, exit with code 1

### 2. Determine Scope

- Check for `--global` flag from parent context
  - If present: Use global store (`~/.ragged_memory/`)
- Check for `--local` flag from parent context
  - If present: Use local store (`.ragged_memory/`)
- If no flag: Use default scope detection
  - If in project directory: Use local store
  - If not in project: Use global store

### 3. Check for Duplicates

- Compute SHA256 hash of file content
- Query LanceDB for existing entries with same `file_hash`
- If found:
  - Show message: "File already indexed (hash: abc123...)"
  - Show timestamp of previous indexing
  - Ask: "Re-index? This will add duplicate chunks. (y/n)"
  - If 'n': Exit cleanly with code 0
  - If 'y': Continue to indexing

### 4. Chunk File

- Initialize Chonkie SemanticChunker with defaults
- Split file content into semantic chunks
- Show progress: "Chunking... {chunk_count} chunks created"

### 5. Generate Embeddings

- Load sentence-transformers model (cached after first load)
- Generate embeddings for all chunks
- Show progress bar if file > 1MB
- Progress: "Generating embeddings... [########--] 80%"

### 6. Store in LanceDB

- Create IndexEntry records for each chunk
- Append to appropriate LanceDB table (local or global)
- Show confirmation: "Indexed {chunk_count} chunks from {filename}"

### 7. Provide Summary

- Display scope indicator (local or global)
- Show file path, chunk count, processing time
- Suggest next steps (search command when available)

## Exit Codes

- `0`: Success (file indexed or skipped by user choice)
- `1`: Error (file not found, not UTF-8, too large, permission denied, storage error)

## Output Examples

### Success (new file)

```bash
$ ram add document.txt
Chunking... 15 chunks created
Generating embeddings... ━━━━━━━━━━━━━━━━━━━━ 100%
✓ Indexed 15 chunks from document.txt

[local: ragged_memory] 15 chunks in 3.2s

Next: Search with 'ram search "query text"'
```

### Success (global scope)

```bash
$ ram --global add ~/notes/ideas.md
Chunking... 42 chunks created
Generating embeddings... ━━━━━━━━━━━━━━━━━━━━ 100%
✓ Indexed 42 chunks from ideas.md

[global] 42 chunks in 7.8s

Next: Search with 'ram search "query text"'
```

### Duplicate detection

```bash
$ ram add document.txt
File already indexed (hash: a3f5c9d2...)
Previously indexed: 2026-02-14 10:30:45

Re-index? This will add duplicate chunks. (y/n): n
Skipped indexing.
```

### Error (file not found)

```bash
$ ram add missing.txt
✗ Error: File 'missing.txt' not found

Check the file path and try again.
```

### Error (not UTF-8)

```bash
$ ram add binary_file.pdf
✗ Error: File 'binary_file.pdf' is not UTF-8 encoded

This command only supports text files. Convert to UTF-8 or use a different tool.
```

### Error (too large)

```bash
$ ram add huge_file.txt
✗ Error: File 'huge_file.txt' is too large (15.3 MB)

Maximum file size: 10 MB. Split the file or remove content.
```

### Error (permission denied)

```bash
$ ram add /root/protected.txt
✗ Error: Permission denied reading '/root/protected.txt'

Check file permissions and try again.
```

## Implementation Notes

- Does NOT require `ram init` to be run first (global store auto-initializes)
- For local scope, creates `.ragged_memory/` if it doesn't exist (if `auto_init_local = true` in config)
- Follows existing scope selection logic from storage infrastructure
- Uses Rich library for progress bars and formatted output
- Processing happens synchronously (no background jobs for prototype)

## Performance Expectations

Based on research benchmarks:

| File Size | Chunk Count | Expected Time |
|-----------|-------------|---------------|
| 10 KB | ~20 chunks | <1 second |
| 100 KB | ~200 chunks | ~5 seconds |
| 1 MB | ~2000 chunks | ~40 seconds |
| 10 MB | ~20000 chunks | ~6-7 minutes |

**Note**: Times assume M1/M2 Mac CPU. Actual times vary based on:
- Content structure (affects chunking)
- CPU speed (affects embedding generation)
- Disk speed (affects storage write)

## Future Enhancements (Out of Scope)

- Batch indexing: `ram add *.txt` or `ram add directory/`
- Update mode: `ram add --update document.txt` (replace existing chunks)
- Remove mode: `ram remove document.txt` (delete chunks)
- Progress persistence: Resume interrupted indexing
- Custom chunk size: `ram add --chunk-size 1024 document.txt`
- Binary file support: PDF, DOCX extraction
- Watch mode: `ram add --watch directory/` (auto-index on change)
