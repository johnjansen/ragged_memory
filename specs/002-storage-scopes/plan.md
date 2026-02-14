# Implementation Plan: Dual Storage Scopes

**Branch**: `002-storage-scopes` | **Date**: 2026-02-14 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-storage-scopes/spec.md`

## Summary

Implement two distinct storage scopes for RAM memories: project-local (`.ragged_memory/` in project root) and user-global (`~/.ragged_memory/` in user home). Use LanceDB for vector storage in both scopes. Provide initialization command to set up project-local storage and centralized configuration via TOML file in global directory.

**Technical approach**: LanceDB stores, TOML configuration, CLI init command, scope detection via directory traversal.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Typer (CLI), LanceDB (vector storage), tomli/tomllib (TOML config)
**Storage**: LanceDB vector database files (one per scope)
**Testing**: Manual validation (per constitution - no automated tests)
**Target Platform**: macOS, Linux (command-line tool)
**Project Type**: Single project (CLI application)
**Performance Goals**: <100ms for scope detection, <500ms for storage initialization
**Constraints**: Must work offline, no external dependencies, local-only storage
**Scale/Scope**: Thousands of memories per scope, multiple projects per user

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**✅ I. Prototype Simplicity**:
- Minimal implementation: Two LanceDB files (local + global), simple TOML config
- No complex abstractions beyond basic Storage class
- Direct file operations, no ORM or repository patterns

**✅ II. No Over-Engineering**:
- No error handling beyond crash-and-fix
- No test infrastructure (manual validation only)
- No abstractions for future requirements (e.g., no plugin system, no migration framework)

**✅ III. Code Clarity**:
- Simple file structure: one module for storage, one for scope detection
- Clear naming: `StorageScope`, `MemoryStore`, `init_project`
- Straightforward logic: check for .ragged_memory/, fall back to global

**✅ IV. File Organization**:
- One class per file: storage.py, scope.py, config.py, init.py
- Files match their primary class/function

**Constitutional Compliance**: ✅ PASS - Implementation aligns with all four core principles

## Project Structure

### Documentation (this feature)

```text
specs/002-storage-scopes/
├── plan.md              # This file
├── research.md          # LanceDB best practices, TOML config patterns
├── data-model.md        # StorageScope, MemoryStore, Config entities
├── quickstart.md        # How to initialize and use storage scopes
└── contracts/           # CLI command signatures
```

### Source Code (repository root)

```text
src/
├── storage/
│   ├── scope.py         # StorageScope class (enum: LOCAL, GLOBAL)
│   ├── store.py         # MemoryStore class (LanceDB wrapper)
│   └── config.py        # Config class (TOML file management)
├── cli/
│   ├── init.py          # `ram init` command implementation
│   └── common.py        # Scope detection utilities
└── models/
    └── memory.py        # Memory entity (text, vector, metadata)

.ragged_memory/          # Project-local storage (created by `ram init`)
└── memories.lance       # LanceDB file for project memories

~/.ragged_memory/        # User-global storage (created automatically)
├── config.toml          # Centralized configuration
└── memories.lance       # LanceDB file for global memories
```

**Structure Decision**: Single project layout. All code under `src/` with logical grouping by concern (storage, cli, models). Storage directories created on-demand at runtime. No tests/ directory per constitution.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

N/A - No constitutional violations. Implementation follows all principles.
