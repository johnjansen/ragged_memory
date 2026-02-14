# CLI Interface Contract

**Feature**: 001-cli-scaffolding
**Date**: 2026-02-14
**Purpose**: Define command-line interface contracts for the RAM CLI

## Overview

This document specifies the CLI interface contracts - the public API users interact with via the command line. Each command definition is a contract that future implementations must honor.

---

## Application Entry Point

### Command: `ram`

**Description**: Main application entry point

**Usage**:
```bash
ram [OPTIONS] COMMAND [ARGS]...
```

**Global Options**:

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--version` | `-v` | flag | - | Show version and exit |
| `--help` | `-h` | flag | - | Show help and exit |

**Behavior**:
- No command provided: Show help message
- Invalid command: Show error + suggest similar commands
- With `--version`: Print version and exit with code 0
- With `--help`: Print help and exit with code 0

**Exit Codes**:
- `0` - Success
- `1` - General error
- `2` - Usage error (invalid arguments)

**Example Output** (`ram --help`):
```
Usage: ram [OPTIONS] COMMAND [ARGS]...

  Ragged Memory (RAM) - Semantic memory for LLMs at the command line.

  Store information once, retrieve it later by meaning.

Options:
  -v, --version   Show version and exit
  -h, --help      Show help message

Commands:
  (Future commands will be listed here)
```

**Example Output** (`ram --version`):
```
Ragged Memory (RAM) version 0.1.0
```

---

## Demo Command (Prototype Only)

### Command: `ram hello`

**Description**: Demo command to verify CLI infrastructure works

**Usage**:
```bash
ram hello [NAME]
```

**Arguments**:

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `NAME` | string | No | "World" | Name to greet |

**Behavior**:
- Prints greeting message with provided name
- Uses Rich formatting (green text for success)
- Exits with code 0 on success

**Examples**:
```bash
$ ram hello
Hello, World!

$ ram hello Alice
Hello, Alice!
```

**Help Output** (`ram hello --help`):
```
Usage: ram hello [OPTIONS] [NAME]

  Say hello to someone.

Arguments:
  [NAME]  Name to greet [default: World]

Options:
  --help  Show this message and exit
```

**Exit Codes**:
- `0` - Success

**Output Format**:
- Plain text with Rich color markup
- Success messages in green: `[green]Hello, {name}![/green]`

---

## Error Handling Contracts

### Contract: Invalid Command

**Trigger**: User provides non-existent command

**Example**:
```bash
$ ram invalidcommand
```

**Expected Output**:
```
Error: No such command 'invalidcommand'.

Did you mean:
  (commands with similar names, if any)

Run 'ram --help' for usage information.
```

**Exit Code**: `2` (usage error)

---

### Contract: Invalid Arguments

**Trigger**: User provides wrong argument types or counts

**Example**:
```bash
$ ram hello arg1 arg2  # Too many arguments
```

**Expected Output**:
```
Error: Got unexpected extra argument (arg2)

Usage: ram hello [OPTIONS] [NAME]

Try 'ram hello --help' for help.
```

**Exit Code**: `2` (usage error)

**Note**: Typer handles this automatically, contract specifies expected behavior.

---

### Contract: General Errors

**Trigger**: Command execution fails

**Pattern**:
```
Error: <specific error message>

<optional context or suggestion>
```

**Format Rules**:
- Use Rich `[red]` for "Error:" prefix
- Be specific about what went wrong
- Provide actionable suggestion when possible
- Don't show stack traces to users (unless verbose mode, future)

**Exit Code**: `1` (general error)

---

## Output Format Contracts

### Standard Output (stdout)

**Purpose**: Normal command output, results, data

**Format**:
- Human-readable text with Rich formatting
- Colors for semantic meaning (green=success, red=error, etc.)
- Structured data as tables when appropriate
- Future: Add `--json` flag for machine-readable output

**Example**:
```bash
$ ram hello Alice
Hello, Alice!  # Green colored text
```

---

### Standard Error (stderr)

**Purpose**: Error messages, warnings, diagnostics

**Format**:
- Errors prefixed with `[red]Error:[/red]`
- Warnings prefixed with `[yellow]Warning:[/yellow]`
- Must be visible even if stdout is redirected

**Example**:
```bash
$ ram invalidcommand 2>&1
Error: No such command 'invalidcommand'.
```

---

### Exit Codes Contract

| Code | Meaning | Usage |
|------|---------|-------|
| `0` | Success | Command completed successfully |
| `1` | General error | Command failed (file not found, operation failed, etc.) |
| `2` | Usage error | Invalid arguments, wrong command, etc. |

**Enforcement**: All commands MUST exit with these codes consistently.

---

## Help System Contracts

### Contract: Command Help

**Trigger**: `ram <command> --help`

**Format**:
```
Usage: ram <command> [OPTIONS] [ARGUMENTS]

  <Command description from docstring>

Arguments:
  <NAME>  <description> [required/optional] [default: value]

Options:
  <--flag>  <description> [default: value]
  --help    Show this message and exit

Examples:
  $ ram <command> example
```

**Requirements**:
- Auto-generated from docstrings (Typer handles this)
- Must list all arguments and options
- Must show default values where applicable
- Must indicate required vs optional

---

### Contract: Application Help

**Trigger**: `ram --help` or `ram` (no command)

**Format**:
```
Usage: ram [OPTIONS] COMMAND [ARGS]...

  <Application description>

Options:
  --version  Show version and exit
  --help     Show help message

Commands:
  <command>  <brief description>
  ...
```

**Requirements**:
- Lists all available commands
- Brief description for each command
- Shows global options first
- Sorted alphabetically (or by priority)

---

## Versioning Contract

### Semantic Versioning

**Format**: `MAJOR.MINOR.PATCH` (e.g., `0.1.0`)

**Rules**:
- MAJOR: Breaking CLI changes (removed commands, changed arguments)
- MINOR: New commands or options (backward compatible)
- PATCH: Bug fixes, no interface changes

**Display**:
```bash
$ ram --version
Ragged Memory (RAM) version 0.1.0
```

**Source of Truth**: `ram/version.py` → `__version__` string

---

## Future Extension Contracts

### Reserved for Future Features

These interfaces are placeholders - not implemented in scaffolding:

**Memory Management Commands** (feature 002+):
```bash
ram store <content> [OPTIONS]   # Store a memory
ram search <query> [OPTIONS]    # Search memories
ram list [OPTIONS]              # List all memories
ram delete <id> [OPTIONS]       # Delete a memory
```

**Scope Management** (feature 002):
```bash
--scope [project|global]        # Explicit scope selection
--project                       # Force project scope
--global                        # Force global scope
```

**Output Formatting** (future):
```bash
--json                          # JSON output
--quiet                         # Minimal output
--verbose                       # Detailed output
```

---

## Contract Validation

### How to Verify Contracts

1. **Manual Testing**:
   ```bash
   # Test help
   ram --help
   ram hello --help

   # Test version
   ram --version

   # Test commands
   ram hello
   ram hello Alice

   # Test errors
   ram nonexistent
   ram hello too many args
   ```

2. **Behavioral Checks**:
   - Help output matches format specifications
   - Exit codes match contract definitions
   - Error messages are clear and actionable
   - Rich formatting renders correctly

3. **Interface Stability**:
   - Once released, contracts cannot change without version bump
   - New options okay (MINOR), removed options are MAJOR
   - Output format changes should be MINOR unless breaking

---

## Contract Compliance

### Implementation Requirements

All commands MUST:
- Have a docstring (for help generation)
- Define type hints for all parameters
- Use Rich console for output
- Exit with appropriate exit codes
- Handle errors gracefully

### Breaking Changes

These require MAJOR version bump:
- Removing a command
- Removing an option
- Changing required arguments
- Changing argument types
- Changing exit code meanings

### Compatible Changes

These require only MINOR version bump:
- Adding a new command
- Adding a new option (with defaults)
- Adding new output features
- Improving error messages
- Adding examples to help

---

## Implementation Notes

### Typer Enforces Contracts

- Typer automatically enforces:
  - Type validation
  - Required vs optional arguments
  - Help generation
  - Error messages for invalid input

- Manual enforcement needed for:
  - Exit codes (must use `raise typer.Exit(code)`)
  - Error message formatting (must use Rich)
  - Output consistency (standardize colors/formats)

### Testing Contracts

**Manual validation approach** (per constitution):
1. Run each command with valid inputs → verify success
2. Run each command with invalid inputs → verify errors
3. Check all help outputs → verify completeness
4. Verify exit codes → use `echo $?` after commands

**No automated tests required** for prototype.

---

## Summary

**CLI Contracts Defined**:
1. Application entry point (`ram`)
2. Global options (--version, --help)
3. Demo command (ram hello)
4. Error handling patterns
5. Output format standards
6. Exit code conventions
7. Help system behavior

**Contract Guarantees**:
- Consistent command structure
- Predictable error handling
- Clear help documentation
- Standard exit codes
- Rich formatted output

**Ready for**: Quickstart guide and implementation
