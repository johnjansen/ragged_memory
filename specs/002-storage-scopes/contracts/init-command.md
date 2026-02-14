# CLI Contract: ram init

**Command**: `ram init`
**Purpose**: Initialize a project-local memory store in the current directory

## Signature

```bash
ram init [OPTIONS]
```

## Options

None (simplest implementation)

## Behavior

1. Check if `.ragged_memory/` already exists in current directory
   - If exists: Print message "Local store already initialized" and exit with code 0
   - If not: Continue to step 2

2. Create `.ragged_memory/` directory in current directory

3. Initialize LanceDB database in `.ragged_memory/`

4. Print success message with next steps

## Exit Codes

- `0`: Success (store initialized or already exists)
- `1`: Error (permission denied, disk full, etc.)

## Output Examples

### Success (new initialization)

```bash
$ ram init
✓ Created .ragged_memory/
✓ Initialized local memory store
✓ Project ready for local memories

Next steps:
  ram store "your memory text"          # Store a memory locally
  ram search "query"                    # Search local memories
  ram store --global "your memory"      # Store globally instead
```

### Success (already initialized)

```bash
$ ram init
✓ Local store already initialized at .ragged_memory/

Use 'ram store' to add memories to this project.
```

### Error (permission denied)

```bash
$ ram init
✗ Error: Permission denied creating .ragged_memory/

Check directory permissions and try again.
```

## Implementation Notes

- Does NOT create global store (that auto-initializes on first use)
- Does NOT require project root detection (initializes in current directory)
- Safe to run multiple times (idempotent)
- Follows convention of other init commands (npm init, git init)
