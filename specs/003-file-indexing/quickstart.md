# Quickstart: File Indexing

**Feature**: 003-file-indexing
**Date**: 2026-02-14

## Overview

This guide shows how to use `ram add` to index text files into your memory store for semantic search.

## Basic Usage

### Index a File Locally

```bash
# In your project directory
cd ~/projects/my-app

# Initialize local storage (if not already done)
ram init

# Index a file
ram add README.md

# Output:
# Chunking... 8 chunks created
# Generating embeddings... ━━━━━━━━━━━━━━━━━━━━ 100%
# ✓ Indexed 8 chunks from README.md
# [local: my-app] 8 chunks in 2.1s
```

### Index a File Globally

```bash
# Index personal notes to global store
ram --global add ~/notes/coding-patterns.md

# Output:
# Chunking... 25 chunks created
# Generating embeddings... ━━━━━━━━━━━━━━━━━━━━ 100%
# ✓ Indexed 25 chunks from coding-patterns.md
# [global] 25 chunks in 5.3s
```

## Common Workflows

### 1. Index Project Documentation

```bash
# Navigate to project
cd ~/projects/ragged_memory

# Initialize local storage
ram init

# Index key documentation
ram add README.md
ram add ARCHITECTURE.md
ram add docs/CONTRIBUTING.md

# All files now searchable within this project context
```

### 2. Build Personal Knowledge Base

```bash
# Index reference materials to global store
ram --global add ~/notes/python-patterns.md
ram --global add ~/notes/git-workflows.md
ram --global add ~/notes/vim-commands.md

# These are now searchable from any directory
cd ~/projects/any-project
ram search "python decorator pattern"  # Finds content from python-patterns.md
```

### 3. Index Code Files

```bash
# Index source files for code search
ram add src/main.py
ram add src/utils.py
ram add src/models/user.py

# Later, find code by description
ram search "user authentication logic"  # Finds relevant code chunks
```

### 4. Mixed Local and Global Content

```bash
# Project-specific
ram add project-notes.md        # Local scope (default in project)
ram add architecture-decisions.md

# Personal reference
ram --global add ~/cheatsheets/docker-commands.md

# When searching:
# - Default search includes local content only
# - Use --global to search personal knowledge base
# - Use --all to search both (future feature)
```

## File Requirements

### Supported Files

✅ **Text files with UTF-8 encoding**:
- Markdown: `.md`, `.markdown`
- Code: `.py`, `.js`, `.java`, `.go`, `.rs`, etc.
- Plain text: `.txt`
- Configuration: `.yaml`, `.json`, `.toml`, `.ini`
- Documentation: `.rst`, `.adoc`

### Unsupported (Will Error)

❌ **Binary files**:
- PDFs: `.pdf`
- Word documents: `.docx`, `.doc`
- Images: `.png`, `.jpg`, `.gif`
- Archives: `.zip`, `.tar`, `.gz`

❌ **Non-UTF-8 text files**:
- Files with Latin-1, ISO-8859-1, or other encodings
- Must convert to UTF-8 before indexing

### Size Limits

- **Maximum**: 10 MB per file
- **Recommended**: < 1 MB for fast processing
- **Large files**: Consider splitting into smaller chunks manually

## Duplicate Handling

```bash
# First time - indexes file
$ ram add document.txt
✓ Indexed 15 chunks from document.txt

# Second time - detects duplicate
$ ram add document.txt
File already indexed (hash: a3f5c9d2...)
Previously indexed: 2026-02-14 10:30:45

Re-index? This will add duplicate chunks. (y/n): n
Skipped indexing.

# Choose 'y' to re-index (useful if chunking logic changes)
```

## Scope Selection

### Automatic Scope Detection

```bash
# Inside project with .ragged_memory/
cd ~/projects/my-app
ram add file.txt          # → Uses local scope

# Outside any project
cd ~/
ram add file.txt          # → Uses global scope
```

### Explicit Scope Control

```bash
# Force local scope
ram --local add file.txt  # Always local, even if outside project

# Force global scope
ram --global add file.txt # Always global, even if in project
```

### When to Use Each Scope

**Local Scope** (`.ragged_memory/`):
- Project documentation (README, ARCHITECTURE)
- Code files from this codebase
- Project-specific notes and decisions
- Issue/ticket descriptions
- Meeting notes about this project

**Global Scope** (`~/.ragged_memory/`):
- Personal cheat sheets and references
- General coding patterns and snippets
- Tool documentation (vim, git, docker)
- Cross-project learnings
- Personal coding style guide

## Error Handling

### File Not Found

```bash
$ ram add nonexistent.txt
✗ Error: File 'nonexistent.txt' not found
```

**Fix**: Check the file path and spelling

### Not UTF-8 Encoded

```bash
$ ram add legacy_file.txt
✗ Error: File 'legacy_file.txt' is not UTF-8 encoded
```

**Fix**: Convert file to UTF-8:
```bash
# Using iconv
iconv -f ISO-8859-1 -t UTF-8 legacy_file.txt > legacy_file_utf8.txt

# Then index
ram add legacy_file_utf8.txt
```

### File Too Large

```bash
$ ram add huge_dataset.csv
✗ Error: File 'huge_dataset.csv' is too large (25.5 MB)
```

**Fix**: Split file into smaller parts:
```bash
# Split into 5MB chunks
split -b 5m huge_dataset.csv dataset_part_

# Index each part
ram add dataset_part_aa
ram add dataset_part_ab
```

### Permission Denied

```bash
$ ram add /root/secret.txt
✗ Error: Permission denied reading '/root/secret.txt'
```

**Fix**: Check file permissions:
```bash
ls -l /root/secret.txt
# Ensure you have read access
```

## Performance Tips

### Fast Processing

For quick indexing:
- Keep files under 100 KB
- Use simple text format (fewer special characters)
- Index during idle time (embedding generation is CPU-intensive)

### Large File Strategy

For files 1-10 MB:
- Expect processing time of 1-10 minutes
- Run during breaks or batch process overnight
- Consider splitting very large files

### Batch Indexing

```bash
# Index multiple files sequentially
for file in docs/*.md; do
    ram add "$file"
done

# Or use find
find docs/ -name "*.md" -exec ram add {} \;
```

**Note**: Future feature will support `ram add docs/*.md` directly

## Verification

### Check Indexing Success

After indexing, verify content is searchable:

```bash
# Index a file
ram add document.txt

# Search for content you know is in the file
ram search "specific phrase from document"

# Should return chunks from document.txt
```

### Inspect Storage

```bash
# Check local storage exists
ls -la .ragged_memory/

# Check global storage exists
ls -la ~/.ragged_memory/

# View LanceDB files
ls -la .ragged_memory/memories.lance/
```

## Next Steps

After indexing files:

1. **Search content**: `ram search "your query"` (when implemented)
2. **List indexed files**: `ram list` (future feature)
3. **Remove indexed files**: `ram remove document.txt` (future feature)
4. **Update indexed files**: Re-run `ram add` after file changes

## Example Session

```bash
# Setup project
cd ~/projects/my-blog
ram init

# Index blog posts
ram add posts/getting-started.md
ram add posts/advanced-tips.md
ram add posts/troubleshooting.md

# Index personal reference globally
ram --global add ~/notes/markdown-syntax.md

# Later, search within project
ram search "troubleshooting database connections"
# Returns: chunks from troubleshooting.md

# Search personal notes
ram --global search "markdown table syntax"
# Returns: chunks from markdown-syntax.md
```

## Troubleshooting

### Model Download

First time running `ram add`, sentence-transformers will download the embedding model (~80 MB):

```bash
$ ram add first-file.txt
Downloading model 'sentence-transformers/all-MiniLM-L6-v2'...
[########################################] 100%
Chunking... 10 chunks created
...
```

**Note**: Subsequent runs use cached model (much faster)

### Storage Space

Each chunk requires ~1-2 KB in LanceDB (text + 384-dim vector). Estimate storage needs:

```
File size (MB) → Chunks → Storage (MB)
0.1 MB → ~200 chunks → ~0.2 MB
1 MB → ~2000 chunks → ~2 MB
10 MB → ~20000 chunks → ~20 MB
```

### Slow Performance

If indexing is slow:
1. Check CPU usage (embedding generation is CPU-bound)
2. Ensure no other heavy processes running
3. Consider splitting large files
4. Verify sufficient RAM available (>2 GB recommended)

## Advanced Usage

### Index with Explicit Paths

```bash
# Relative paths
ram add ../shared/README.md
ram add ./docs/api.md

# Absolute paths
ram add /Users/john/documents/notes.txt

# Paths with spaces
ram add "my document.txt"
```

### Selective Indexing

```bash
# Only index specific sections
# (Manual approach for prototype)
head -n 100 large_file.txt > excerpt.txt
ram add excerpt.txt
rm excerpt.txt

# Or use grep to extract relevant sections
grep -A 10 "Important Section" document.txt > important.txt
ram add important.txt
```

## FAQ

**Q: Can I index the same file to both local and global?**
A: Yes! The file will have separate chunk entries in each scope.

```bash
ram add file.txt           # Local scope
ram --global add file.txt  # Global scope (duplicate)
```

**Q: What happens if I edit a file after indexing?**
A: Old chunks remain. Re-run `ram add` to index the updated version (creates duplicates). Future feature will handle updates.

**Q: Can I remove indexed files?**
A: Not yet - this is a future feature. For now, indexed chunks persist.

**Q: Does indexing modify the original file?**
A: No, the original file is never modified. RAM only reads the file.

**Q: Can I see which files are indexed?**
A: Not yet - this is a future feature (`ram list` command).

**Q: What's the best chunk size?**
A: The default (512 tokens) balances context vs embedding limits. This is not configurable in the prototype.
