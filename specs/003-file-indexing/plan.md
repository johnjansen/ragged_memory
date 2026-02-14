# Implementation Plan: File Indexing and Embedding

**Branch**: `003-file-indexing` | **Date**: 2026-02-14 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/003-file-indexing/spec.md`

## Summary

Implement file indexing command (`ram add <file>`) that reads UTF-8 text files, intelligently chunks them using Chonkie's SemanticChunker, generates embeddings, and stores chunks in LanceDB (local or global scope). Each chunk maintains reference to its source file and contains the full text content to enable question-answering without accessing the original file.

**Technical approach**: Chonkie SemanticChunker for intelligent text splitting, sentence-transformers for embeddings, LanceDB for vector storage with metadata.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Chonkie (semantic chunking), sentence-transformers (embeddings), LanceDB (vector storage), typer (CLI)
**Storage**: LanceDB vector database files (existing: .ragged_memory/ and ~/.ragged_memory/)
**Testing**: Manual validation (per constitution - no automated tests)
**Target Platform**: macOS, Linux (command-line tool)
**Project Type**: Single project (CLI application extending existing RAM codebase)
**Performance Goals**: <5 seconds for 100KB files, handle files up to 10MB
**Constraints**: UTF-8 encoding only, offline-capable, no external API dependencies
**Scale/Scope**: Individual files up to 10MB, thousands of chunks per file, local processing only

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**✅ I. Prototype Simplicity**:
- Minimal implementation: Use Chonkie's SemanticChunker out-of-the-box, sentence-transformers default model
- Direct file reading with basic error handling
- No custom chunking algorithms or optimization

**✅ II. No Over-Engineering**:
- No automated tests (manual validation only)
- No error handling beyond crash-and-fix
- No abstractions for future requirements (no plugin system for different chunkers)
- Use Chonkie's defaults, no custom configuration UI

**✅ III. Code Clarity**:
- Simple file structure: one module for chunking, one for embedding, one for CLI command
- Clear naming: `FileChunker`, `EmbeddingGenerator`, `add_command`
- Straightforward logic: read file → chunk → embed → store

**✅ IV. File Organization**:
- One class per file: chunker.py, embedder.py, add.py
- Files match their primary class/function

**Constitutional Compliance**: ✅ PASS - Implementation aligns with all four core principles

## Project Structure

### Documentation (this feature)

```text
specs/003-file-indexing/
├── plan.md              # This file
├── research.md          # Chonkie patterns, embedding strategies
├── data-model.md        # Chunk, IndexEntry, FileMetadata entities
├── quickstart.md        # How to use ram add command
└── contracts/           # CLI command signatures
    └── add-command.md
```

### Source Code (repository root)

```text
ram/
├── indexing/
│   ├── __init__.py
│   ├── chunker.py       # FileChunker class (Chonkie integration)
│   ├── embedder.py      # EmbeddingGenerator class (sentence-transformers)
│   └── indexer.py       # FileIndexer class (orchestrates chunk → embed → store)
├── cli/
│   └── commands/
│       ├── init.py      # Existing
│       ├── demo.py      # Existing
│       └── add.py       # NEW: ram add command
├── storage/
│   ├── scope.py         # Existing
│   ├── config.py        # Existing
│   ├── store.py         # Existing - EXTEND for chunk storage
│   ├── context.py       # Existing
│   └── manager.py       # Existing
└── models/
    └── chunk.py         # NEW: Chunk dataclass

pyproject.toml           # Add chonkie, sentence-transformers dependencies
```

**Structure Decision**: Single project layout. All code under `ram/` with logical grouping by concern (indexing, cli, storage, models). New `indexing/` module for chunking and embedding. No tests/ directory per constitution.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

N/A - No constitutional violations. Implementation follows all principles.
