# Tasks: CLI Application Foundation

**Input**: Design documents from `/specs/001-cli-scaffolding/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/

**Tests**: Per Constitution: Tests are NOT required for prototypes - only include if explicitly requested.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `ram/`, repository root
- Paths shown below assume single project layout from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure (ram/, ram/cli/, ram/cli/commands/)
- [X] T002 Create pyproject.toml with metadata and dependencies (typer[all]>=0.9.0)
- [X] T003 [P] Create .gitignore file for Python project (__pycache__, *.pyc, .venv, dist/, build/)
- [X] T004 [P] Create ram/__init__.py to mark as package
- [X] T005 [P] Create ram/cli/__init__.py to mark CLI subpackage
- [X] T006 [P] Create ram/cli/commands/__init__.py for command modules
- [X] T007 [P] Create ram/version.py with __version__ = "0.1.0"

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T008 Create ram/cli/app.py with Typer application instance and Rich console
- [X] T009 Create ram/__main__.py entry point that calls app() from cli/app.py
- [X] T010 Implement main callback in ram/cli/app.py for global options handling

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Command Discovery (Priority: P1) 🎯 MVP

**Goal**: Users can discover available commands and get help without external documentation

**Independent Test**: Run `ram` with no args, `ram --help`, and `ram --version` to verify output

### Implementation for User Story 1

- [X] T011 [US1] Implement version callback function in ram/cli/app.py
- [X] T012 [US1] Add --version/-v eager option to main callback in ram/cli/app.py
- [X] T013 [US1] Configure Typer app with no_args_is_help=True in ram/cli/app.py
- [X] T014 [US1] Add application help text and description to Typer app in ram/cli/app.py
- [X] T015 [US1] Create demo command in ram/cli/commands/demo.py for testing command discovery
- [X] T016 [US1] Register demo command with app in ram/cli/app.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently
- Running `ram` shows help with available commands
- Running `ram --help` shows comprehensive usage
- Running `ram --version` shows version number

---

## Phase 4: User Story 2 - Command Execution Framework (Priority: P2)

**Goal**: Users can execute commands with arguments and options, with proper validation and error handling

**Independent Test**: Invoke demo command with various argument combinations and verify correct parsing

### Implementation for User Story 2

- [X] T017 [US2] Add required argument to demo command in ram/cli/commands/demo.py
- [X] T018 [US2] Add optional flag to demo command in ram/cli/commands/demo.py
- [X] T019 [US2] Implement argument validation in ram/cli/commands/demo.py
- [X] T020 [US2] Add error handling for invalid arguments in ram/cli/commands/demo.py
- [X] T021 [US2] Use Rich console for formatted output in ram/cli/commands/demo.py
- [X] T022 [US2] Test command execution with valid arguments manually
- [X] T023 [US2] Test command execution with invalid arguments manually (verify error messages)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently
- Commands execute with correct argument parsing
- Invalid input shows clear error messages
- Optional flags are recognized and applied

---

## Phase 5: User Story 3 - Command-Level Help (Priority: P3)

**Goal**: Users get detailed help for specific commands with examples and option documentation

**Independent Test**: Run `ram demo --help` and verify comprehensive command-specific help

### Implementation for User Story 3

- [X] T024 [US3] Add comprehensive docstring to demo command in ram/cli/commands/demo.py
- [X] T025 [US3] Document all arguments with descriptions in ram/cli/commands/demo.py
- [X] T026 [US3] Document all options with help text in ram/cli/commands/demo.py
- [X] T027 [US3] Add usage examples to demo command docstring in ram/cli/commands/demo.py
- [X] T028 [US3] Verify command help output manually with `ram demo --help`

**Checkpoint**: All user stories should now be independently functional
- Each command provides detailed help
- Arguments and options are documented
- Usage examples guide users

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T029 [P] Update README.md with installation instructions and quick start
- [X] T030 [P] Verify all commands have proper docstrings and type hints
- [X] T031 Verify application responds within 100ms (manual timing test)
- [X] T032 Test CLI from different directories to verify it works anywhere
- [X] T033 Verify exit codes: 0 for success, non-zero for errors
- [X] T034 Test edge cases from spec (no write permissions, malformed input, etc.)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on US1, but builds on the same demo command
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Enhances commands created in US1/US2

### Within Each User Story

- Setup tasks (T001-T007) can run in parallel where marked [P]
- Foundational tasks (T008-T010) must complete sequentially
- US1 tasks (T011-T016) must run sequentially (each builds on previous)
- US2 tasks (T017-T023) can partially parallelize (e.g., T022-T023 are manual tests)
- US3 tasks (T024-T028) must run sequentially (documentation tasks)
- Polish tasks (T029-T034) marked [P] can run in parallel

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003-T007)
- Within Foundational phase: T008-T009 sequential, but can prepare in parallel
- Different user stories can be worked on in parallel by different team members after Phase 2
- Polish tasks marked [P] can run in parallel (T029-T030)

---

## Parallel Example: Setup Phase

```bash
# Launch all parallel setup tasks together:
Task: "Create .gitignore file for Python project"
Task: "Create ram/__init__.py to mark as package"
Task: "Create ram/cli/__init__.py to mark CLI subpackage"
Task: "Create ram/cli/commands/__init__.py for command modules"
Task: "Create ram/version.py with __version__"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T007)
2. Complete Phase 2: Foundational (T008-T010) - CRITICAL
3. Complete Phase 3: User Story 1 (T011-T016)
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Run `ram` → should show help
   - Run `ram --help` → should show detailed help
   - Run `ram --version` → should show version
   - Run `ram demo` → command should exist (basic test)
5. MVP complete - foundation ready for other features

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → MVP complete! 🎯
3. Add User Story 2 → Test independently → Enhanced execution
4. Add User Story 3 → Test independently → Full help system
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (T011-T016)
   - Developer B: User Story 2 (T017-T023) - starts after US1 T015-T016 complete (need demo command)
   - Developer C: User Story 3 (T024-T028) - starts after US2 complete (need fully functional commands)
3. Note: US2 and US3 depend on US1 creating the demo command, so true parallelization limited here
4. Alternative: Create separate demo commands per developer to enable parallel work

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- No tests directory or test tasks (per Constitution: tests NOT required for prototypes)
- Manual validation through running commands and observing output
- Commit after completing each phase
- Stop at any checkpoint to validate story independently
- File paths are specific (not "create a file" but "create ram/cli/app.py")
- Avoid: vague tasks, same file conflicts, unclear acceptance criteria

---

## Manual Validation Checkpoints

Since automated tests are not required (per Constitution), validate manually at these checkpoints:

**After Phase 2 (Foundational)**:
- `python -m ram` should import without errors
- Typer app should be created successfully

**After Phase 3 (US1)**:
- `ram` with no args shows help
- `ram --help` shows detailed help
- `ram --version` shows version number
- Help output is well-formatted (Rich rendering)

**After Phase 4 (US2)**:
- `ram demo "test"` executes successfully
- `ram demo "test" --verbose` recognizes flag
- `ram demo` with no args shows error + help
- Invalid arguments show clear error messages

**After Phase 5 (US3)**:
- `ram demo --help` shows comprehensive help
- All arguments documented with descriptions
- All options documented with defaults
- Usage examples visible in help

**After Phase 6 (Polish)**:
- README has installation + quickstart
- All commands respond < 100ms
- Works from any directory
- Exit codes correct (0=success, 1=error)
