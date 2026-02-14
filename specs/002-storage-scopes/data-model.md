# Data Model: Dual Storage Scopes

**Feature**: 002-storage-scopes
**Date**: 2026-02-14

## Entities

### StorageScope (Enum)

Defines the visibility boundary for stored memories.

**Values**:
- `LOCAL`: Project-local scope (`.ragged_memory/`)
- `GLOBAL`: User-global scope (`~/.ragged_memory/`)

**Usage**:
```python
from enum import Enum

class StorageScope(Enum):
    LOCAL = "local"
    GLOBAL = "global"
```

---

### Config

Centralized configuration loaded from `~/.ragged_memory/config.toml`.

**Attributes**:
- `embedding_model` (str): Model name for embeddings (default: "sentence-transformers/all-MiniLM-L6-v2")
- `vector_dimensions` (int): Dimension of embedding vectors (default: 384)
- `default_scope` (StorageScope): Default scope when unspecified (default: LOCAL)
- `auto_init_local` (bool): Auto-create .ragged_memory/ on first store (default: true)
- `global_dir` (Path): Global storage directory (default: ~/.ragged_memory)
- `local_dir` (str): Local storage directory name (default: .ragged_memory)

**File Structure** (~/.ragged_memory/config.toml):
```toml
[storage]
embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
vector_dimensions = 384

[scope]
default_scope = "local"
auto_init_local = true

[paths]
global_dir = "~/.ragged_memory"
local_dir = ".ragged_memory"
```

**Class Structure**:
```python
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Config:
    embedding_model: str
    vector_dimensions: int
    default_scope: StorageScope
    auto_init_local: bool
    global_dir: Path
    local_dir: str

    @classmethod
    def load(cls, config_path: Path) -> "Config":
        """Load config from TOML file, use defaults if missing"""
        pass
```

---

### MemoryStore

A persistent collection of memories with a specific scope and storage location.

**Attributes**:
- `scope` (StorageScope): The scope of this store (LOCAL or GLOBAL)
- `db_path` (Path): Path to the LanceDB database directory
- `table_name` (str): Name of the LanceDB table (default: "memories")
- `is_initialized` (bool): Whether the store has been initialized

**Methods**:
- `initialize()`: Create storage directory and LanceDB table
- `exists()`: Check if store is already initialized
- `get_path()`: Return the full path to the store

**Class Structure**:
```python
from pathlib import Path
import lancedb

class MemoryStore:
    def __init__(self, scope: StorageScope, db_path: Path):
        self.scope = scope
        self.db_path = db_path
        self.table_name = "memories"

    def initialize(self) -> None:
        """Create directory and initialize LanceDB table"""
        self.db_path.mkdir(parents=True, exist_ok=True)
        db = lancedb.connect(str(self.db_path))
        # Table creation happens on first insert

    def exists(self) -> bool:
        """Check if store directory exists"""
        return self.db_path.exists()

    def get_path(self) -> Path:
        """Get full path to the store"""
        return self.db_path
```

---

### ProjectContext

Represents the current project directory and its associated local store.

**Attributes**:
- `project_root` (Path | None): Root directory of the project, or None if no project detected
- `store_path` (Path): Path to the local `.ragged_memory/` directory

**Methods**:
- `detect()`: Detect project root by searching upward for markers
- `has_local_store()`: Check if project has a local store initialized

**Detection Logic**:
```python
from pathlib import Path

class ProjectContext:
    def __init__(self, start_dir: Path = Path.cwd()):
        self.project_root = self._detect_project_root(start_dir)
        self.store_path = self.project_root / ".ragged_memory" if self.project_root else None

    def _detect_project_root(self, start_dir: Path) -> Path | None:
        """Search upward for .ragged_memory/ or .git/"""
        current = start_dir.absolute()
        while current != current.parent:
            if (current / ".ragged_memory").exists():
                return current
            if (current / ".git").exists():
                return current
            current = current.parent
        return None

    def has_local_store(self) -> bool:
        """Check if project has local store"""
        return self.store_path and self.store_path.exists()
```

---

## Relationships

```
Config (global singleton)
  └─> defines default scope and paths

StorageScope (enum)
  ├─> used by MemoryStore
  └─> used by CLI commands

MemoryStore (2 instances)
  ├─> LOCAL scope → .ragged_memory/memories.lance
  └─> GLOBAL scope → ~/.ragged_memory/memories.lance

ProjectContext (per-session)
  └─> determines if LOCAL scope is available
```

## Data Flow

```
User runs command
      ↓
Detect scope (ProjectContext + flags)
      ↓
Load Config (from ~/.ragged_memory/config.toml)
      ↓
Select MemoryStore (LOCAL or GLOBAL)
      ↓
Initialize if needed (MemoryStore.initialize())
      ↓
Perform operation (store/search/list)
```

## Storage Layout

```
~/.ragged_memory/               # Global scope
├── config.toml                 # Configuration
└── memories.lance/             # LanceDB database
    ├── data/
    ├── index/
    └── metadata/

<project-root>/.ragged_memory/  # Local scope
└── memories.lance/             # LanceDB database
    ├── data/
    ├── index/
    └── metadata/
```

## State Transitions

### Store Initialization

```
NOT_EXISTS → (ram init) → INITIALIZED → (ram store) → HAS_DATA
```

### Scope Selection

```
User in project dir + no flag → LOCAL
User in project dir + --global → GLOBAL
User outside project + no flag → GLOBAL (fallback)
User anywhere + --local → LOCAL (error if no project)
```

## Validation Rules

1. **Local store requires project context**:
   - Cannot use LOCAL scope outside a project
   - Must run `ram init` first or be in directory with `.ragged_memory/`

2. **Global store always available**:
   - Auto-initializes on first use
   - No explicit init required

3. **Config file is optional**:
   - Uses defaults if config.toml missing
   - Invalid config values fall back to defaults

4. **Store paths are immutable**:
   - Cannot change store location after initialization
   - Moving project directory is supported (stores move with it)
   - Moving user home directory requires manual migration (out of scope)
