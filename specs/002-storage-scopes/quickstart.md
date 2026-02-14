# Quickstart: Dual Storage Scopes

**Feature**: 002-storage-scopes
**Audience**: Developers implementing or testing this feature

## Overview

This feature implements two storage scopes for RAM memories:
- **Local**: Project-specific memories (`.ragged_memory/` in project root)
- **Global**: Personal memories (` ~/.ragged_memory/` in user home)

## Setup

### 1. Initialize Global Store (Automatic)

Global store auto-initializes on first use. No setup required.

```bash
# First global operation creates ~/.ragged_memory/
ram store --global "my first global memory"
```

### 2. Initialize Project Store (Manual)

Run `ram init` in your project root:

```bash
cd ~/projects/my-project
ram init
# Creates .ragged_memory/ in current directory
```

## Usage Patterns

### Storing Memories

**Store locally (project-specific)**:
```bash
cd ~/projects/my-project
ram store "This project uses FastAPI for REST APIs"
# Saved to .ragged_memory/
```

**Store globally (personal knowledge)**:
```bash
ram store --global "I prefer pytest over unittest"
# Saved to ~/.ragged_memory/
```

### Searching Memories

**Search locally**:
```bash
cd ~/projects/my-project
ram search "API framework"
# Searches .ragged_memory/ only
```

**Search globally**:
```bash
ram search --global "testing framework"
# Searches ~/.ragged_memory/ only
```

**Search both scopes**:
```bash
ram search --all "framework"
# Searches both local and global
```

## Common Workflows

### Workflow 1: New Project Setup

```bash
# Create new project
mkdir ~/projects/new-project
cd ~/projects/new-project
git init

# Initialize local memory store
ram init

# Store project-specific context
ram store "Python 3.11 microservice using FastAPI"
ram store "Database: PostgreSQL with SQLAlchemy"
ram store "Deployment: Docker on AWS ECS"

# Verify local memories
ram list
```

### Workflow 2: Working Across Projects

```bash
# Store personal preference globally
ram store --global "Always use type hints in Python"

# In project A
cd ~/projects/project-a
ram store "Auth uses JWT with 24h expiry"

# In project B
cd ~/projects/project-b
ram store "Auth uses session cookies"

# Personal preference available everywhere
ram search --global "type hints"
# Returns: "Always use type hints in Python"

# Project-specific auth is isolated
cd ~/projects/project-a
ram search "auth"
# Returns: "Auth uses JWT with 24h expiry"

cd ~/projects/project-b
ram search "auth"
# Returns: "Auth uses session cookies"
```

### Workflow 3: Scope Selection

```bash
cd ~/projects/my-project

# Default: uses local (if initialized)
ram store "memory"
# → .ragged_memory/

# Explicit global (from anywhere)
ram store --global "memory"
# → ~/.ragged_memory/

# Explicit local (must be in project)
ram store --local "memory"
# → .ragged_memory/ (or error if not initialized)
```

## Verification

### Check Store Locations

```bash
# Local store
ls .ragged_memory/
# Should see: memories.lance/

# Global store
ls ~/.ragged_memory/
# Should see: config.toml, memories.lance/
```

### Verify Isolation

```bash
# Store locally in project A
cd ~/projects/project-a
ram init
ram store "Project A memory"

# Store locally in project B
cd ~/projects/project-b
ram init
ram store "Project B memory"

# Verify isolation
cd ~/projects/project-a
ram search "Project B"
# Should return: No results (isolated)

cd ~/projects/project-b
ram search "Project A"
# Should return: No results (isolated)
```

## Configuration

Edit `~/.ragged_memory/config.toml` to customize behavior:

```toml
[scope]
default_scope = "local"      # "local" or "global"
auto_init_local = true       # Auto-create .ragged_memory/ on first store

[paths]
global_dir = "~/.ragged_memory"
local_dir = ".ragged_memory"
```

## Troubleshooting

### Issue: "No project found" error

**Problem**: Using `--local` flag outside a project

**Solution**:
```bash
# Either initialize local store
ram init

# Or use global store instead
ram store --global "memory"
```

### Issue: Memories not found

**Problem**: Wrong scope selected

**Solution**:
```bash
# Check which scope you're searching
ram list           # Local (if in project)
ram list --global  # Global
ram list --all     # Both scopes
```

### Issue: Store not initialized

**Problem**: `.ragged_memory/` doesn't exist

**Solution**:
```bash
# Initialize local store
ram init

# Or use global (auto-initializes)
ram store --global "memory"
```

## Implementation Checklist

For developers implementing this feature:

- [ ] `StorageScope` enum (LOCAL, GLOBAL)
- [ ] `Config` class with TOML loading
- [ ] `MemoryStore` class with LanceDB integration
- [ ] `ProjectContext` with upward directory search
- [ ] `ram init` command implementation
- [ ] `--global` / `-g` flag on all memory commands
- [ ] `--local` / `-l` flag on all memory commands
- [ ] Scope indication in command output
- [ ] Auto-initialization of global store
- [ ] Error handling for missing local store

## Next Steps

After implementing storage scopes:

1. Test with multiple projects (verify isolation)
2. Test global scope from various directories
3. Test scope flags override default behavior
4. Verify config.toml is loaded correctly
5. Test `ram init` idempotency

Then proceed to next features:
- Memory storage and retrieval (store/search commands)
- Semantic search (embeddings and vector similarity)
