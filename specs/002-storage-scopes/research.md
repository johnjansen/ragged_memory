# Research: Dual Storage Scopes

**Feature**: 002-storage-scopes
**Date**: 2026-02-14

## Research Questions

1. How to implement dual storage scopes with LanceDB?
2. Best practices for TOML configuration management?
3. How to detect project boundaries reliably?
4. LanceDB file structure and initialization patterns?

## Decisions

### 1. LanceDB for Vector Storage

**Decision**: Use LanceDB with separate database files for each scope (`.ragged_memory/memories.lance` for local, `~/.ragged_memory/memories.lance` for global)

**Rationale**:
- LanceDB is file-based (perfect for local storage, no server required)
- Native Python support with simple API
- Built for vector similarity search (core RAM requirement)
- Lightweight and fast for small-to-medium datasets (thousands of memories)
- No dependencies on external services (offline-capable)

**Alternatives Considered**:
- **Chroma**: More complex, requires more dependencies
- **SQLite + numpy**: Manual vector operations, more code to maintain
- **Plain files + pickle**: No vector search capability, would need custom implementation

**Implementation approach**:
```python
import lancedb

# Global store
db = lancedb.connect("~/.ragged_memory")
table = db.open_table("memories")

# Local store
db = lancedb.connect(".ragged_memory")
table = db.open_table("memories")
```

### 2. TOML Configuration File

**Decision**: Single `~/.ragged_memory/config.toml` file for global configuration

**Rationale**:
- TOML is Python-native (tomllib in stdlib 3.11+, tomli for older)
- Human-readable and editable
- Standard for Python projects (pyproject.toml pattern)
- Simple key-value structure sufficient for configuration needs

**Configuration structure**:
```toml
[storage]
embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
vector_dimensions = 384

[scope]
default_scope = "local"  # or "global"
auto_init_local = true   # Create .ragged_memory/ automatically

[paths]
global_dir = "~/.ragged_memory"
local_dir = ".ragged_memory"
```

**Alternatives Considered**:
- **JSON**: Less human-friendly, no comments
- **YAML**: Extra dependency, over-engineered for our needs
- **INI**: Less structured, no nested config support

### 3. Project Boundary Detection

**Decision**: Traverse upward from current directory looking for `.ragged_memory/` directory or git root

**Rationale**:
- Simple and reliable
- Follows convention (similar to git, node_modules, virtualenv patterns)
- Users can explicitly mark project root with `.ragged_memory/`
- Fallback to current directory if no project markers found

**Detection algorithm**:
```python
def detect_project_root(start_dir: Path) -> Path | None:
    current = start_dir.absolute()
    while current != current.parent:
        if (current / ".ragged_memory").exists():
            return current
        if (current / ".git").exists():
            return current
        current = current.parent
    return None  # No project found, use global scope
```

**Alternatives Considered**:
- **Git-only detection**: Fails for non-git projects
- **Explicit config flag**: More user friction
- **Current directory only**: No support for subdirectories

### 4. Storage Initialization Pattern

**Decision**: `ram init` command creates `.ragged_memory/` in current directory and initializes LanceDB

**Rationale**:
- Explicit user control (no surprise directory creation)
- Follows convention (npm init, git init, etc.)
- Clear signal that directory is now a "RAM project"
- Safe (doesn't modify existing data)

**Init command behavior**:
```bash
$ ram init
✓ Created .ragged_memory/
✓ Initialized local memory store
✓ Project ready for local memories

# Global store auto-initializes on first use
$ ram store --global "my memory"
✓ Created ~/.ragged_memory/
✓ Initialized global memory store
✓ Stored memory (scope: global)
```

**Alternatives Considered**:
- **Auto-init on first store**: Less explicit, could surprise users
- **Manual directory creation**: Too low-level, error-prone
- **Config file init**: Over-engineered for simple directory creation

## Technical Dependencies

### Core Libraries

1. **LanceDB** (`lancedb`): Vector database, file-based storage
2. **Typer**: CLI framework (from 001-cli-scaffolding)
3. **tomli/tomllib**: TOML parsing (stdlib in 3.11+, tomli for older Python)

### Optional/Future

- Sentence transformers for embeddings (separate feature)
- Rich for CLI output formatting (if needed for UX)

## Performance Considerations

**Scope Detection**:
- File system traversal: ~1-10ms for typical project depths (<10 levels)
- Target: <100ms worst case

**Storage Initialization**:
- LanceDB file creation: ~50-200ms
- TOML config read: <10ms
- Target: <500ms for init command

**Memory Operations**:
- Store: Depends on embedding (separate feature)
- Query: LanceDB vector search (sub-100ms for <10k memories)

## Open Questions

None - all research questions resolved with simple, constitutional approaches.
