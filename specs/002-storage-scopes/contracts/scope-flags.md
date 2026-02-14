# CLI Contract: Scope Selection Flags

**Purpose**: Allow users to explicitly control storage scope for any command

## Global Flags

These flags apply to all memory commands (store, search, list, etc.)

### --global / -g

**Purpose**: Force global scope regardless of location

```bash
ram store --global "memory text"
ram search --global "query"
ram list --global
```

**Behavior**:
- Overrides default scope detection
- Uses `~/.ragged_memory/` store
- Auto-initializes global store if not exists
- Works from any directory

### --local / -l

**Purpose**: Force local scope, error if no project

```bash
ram store --local "memory text"
ram search --local "query"
ram list --local
```

**Behavior**:
- Overrides default scope detection
- Requires project context (`.ragged_memory/` must exist)
- Errors if no project detected
- Must run `ram init` first if project not initialized

## Default Scope Behavior

When neither flag is specified:

```bash
ram store "memory text"  # Uses default scope
```

**Logic**:
1. Detect project context (search upward for `.ragged_memory/` or `.git/`)
2. If project detected AND has local store → use LOCAL
3. If project detected but NO local store → use GLOBAL (with warning)
4. If no project detected → use GLOBAL

## Scope Indication in Output

All commands MUST indicate which scope was used:

```bash
$ ram store "my memory"
✓ Stored memory (scope: local, project: ragged_memory)

$ ram store --global "my memory"
✓ Stored memory (scope: global)

$ ram search "query"
Found 3 results (scope: local, project: ragged_memory)
...

$ ram search --global "query"
Found 5 results (scope: global)
...
```

## Error Messages

### No project when --local specified

```bash
$ ram store --local "memory"
✗ Error: No project found

Run 'ram init' to initialize a local store, or use --global flag.
```

### Conflicting flags (both --local and --global)

```bash
$ ram store --local --global "memory"
✗ Error: Cannot specify both --local and --global

Use one scope flag at a time.
```

## Implementation Notes

- Flags are mutually exclusive
- Default behavior prioritizes local over global when project detected
- Warning message when defaulting to global despite being in a project
- Clear indication of active scope in all output
