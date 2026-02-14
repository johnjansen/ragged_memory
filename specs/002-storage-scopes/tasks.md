# Tasks: Dual Storage Scopes

**Input**: Design documents from `/specs/002-storage-scopes/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/

**Tests**: Per Constitution: Tests are NOT required for prototypes - only include if explicitly requested.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `ram/storage/`, `ram/cli/`, repository root
- Paths shown below assume single project layout from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project dependencies and basic structure for storage

- [x] T001 Update pyproject.toml with new dependencies (lancedb, tomli for Python <3.11)
- [x] T002 [P] Create ram/storage/ directory for storage modules
- [x] T003 [P] Create ram/storage/__init__.py to mark as package

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core storage infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create StorageScope enum in ram/storage/scope.py (LOCAL, GLOBAL values)
- [x] T005 Create Config dataclass in ram/storage/config.py with TOML loading
- [x] T006 Create MemoryStore class in ram/storage/store.py with LanceDB integration
- [x] T007 Create ProjectContext class in ram/storage/context.py for project detection
- [x] T008 Implement project root detection logic in ProjectContext (search for .ragged_memory/ or .git/)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Project-Local Memory Storage (Priority: P1) 🎯 MVP

**Goal**: Users can initialize and use project-local memory stores with automatic scope detection

**Independent Test**: Run `ram init` in project directory, verify .ragged_memory/ created and isolated from other projects

### Implementation for User Story 1

- [x] T009 [US1] Create ram/cli/commands/init.py module for init command
- [x] T010 [US1] Implement init command function in ram/cli/commands/init.py
- [x] T011 [US1] Add check for existing .ragged_memory/ in init command
- [x] T012 [US1] Implement directory creation (.ragged_memory/) in init command
- [x] T013 [US1] Initialize LanceDB store in .ragged_memory/ in init command
- [x] T014 [US1] Add success/error messages with Rich formatting in init command
- [x] T015 [US1] Register init command with main app in ram/cli/app.py
- [x] T016 [US1] Test init command manually (ram init in test directory)
- [x] T017 [US1] Test init command idempotency (run twice, should not error)
- [x] T018 [US1] Verify .ragged_memory/ directory created with correct structure

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently
- Running `ram init` creates .ragged_memory/ directory
- Re-running `ram init` shows "already initialized" message
- Directory structure matches plan.md specifications

---

## Phase 4: User Story 2 - User-Global Memory Storage (Priority: P2)

**Goal**: Users can access global memory store from any directory with automatic initialization

**Independent Test**: Access global scope from multiple directories, verify same data accessible everywhere

### Implementation for User Story 2

- [x] T019 [US2] Implement global directory detection in ram/storage/context.py
- [x] T020 [US2] Add get_global_dir() method to Config class in ram/storage/config.py
- [x] T021 [US2] Implement auto-initialization for global store in MemoryStore class
- [x] T022 [US2] Create ~/.ragged_memory/ directory on first global access
- [x] T023 [US2] Initialize default config.toml in ~/.ragged_memory/
- [x] T024 [US2] Initialize LanceDB store in ~/.ragged_memory/
- [x] T025 [US2] Test global store initialization manually (access from any directory)
- [x] T026 [US2] Verify global store accessible from multiple directories
- [x] T027 [US2] Verify config.toml created with default values

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently
- Local stores isolated per project
- Global store accessible from anywhere
- Auto-initialization works for global scope

---

## Phase 5: User Story 3 - Scope Selection Control (Priority: P3)

**Goal**: Users can explicitly control scope with --global/--local flags and see which scope is active

**Independent Test**: Use scope flags with commands, verify correct scope used and indicated in output

### Implementation for User Story 3

- [x] T028 [US3] Add scope detection utility functions to ram/cli/common.py
- [x] T029 [US3] Implement get_active_scope() function in ram/cli/common.py
- [x] T030 [US3] Add --global/-g option to main callback in ram/cli/app.py
- [x] T031 [US3] Add --local/-l option to main callback in ram/cli/app.py
- [x] T032 [US3] Implement scope flag validation (mutually exclusive) in ram/cli/app.py
- [x] T033 [US3] Add scope indication to command output in ram/cli/app.py
- [x] T034 [US3] Update init command to respect --local flag in ram/cli/commands/init.py
- [x] T035 [US3] Test --global flag manually (ram init --global should error appropriately)
- [x] T036 [US3] Test --local flag manually (ram init --local should work)
- [x] T037 [US3] Test conflicting flags (--global --local should error)
- [x] T038 [US3] Verify scope indication appears in all command outputs

**Checkpoint**: All user stories should now be independently functional
- Scope flags work correctly
- Default scope detection works
- Output clearly indicates active scope
- Error messages for invalid flag combinations

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T039 [P] Add comprehensive docstrings to all storage classes
- [x] T040 [P] Update README.md with storage scope documentation
- [x] T041 Verify scope isolation (project stores don't leak)
- [x] T042 Verify global store user isolation (different users can't access each other's data)
- [x] T043 Test scope detection performance (<100ms as per plan)
- [x] T044 Test storage initialization performance (<500ms as per plan)
- [x] T045 Test edge cases: no write permissions, disk full, moved project directory
- [x] T046 Verify config.toml defaults match spec
- [x] T047 Create example project demonstrating scope usage
- [x] T048 Validate all paths resolve correctly (handle ~, relative paths)

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1 (but shares same classes)
- **User Story 3 (P3)**: Depends on US1 and US2 being complete (adds flags to existing functionality)

### Within Each User Story

- Foundational classes must exist before any user story (Phase 2 gates all)
- US1: Init command → Directory creation → Store initialization → Testing
- US2: Global detection → Auto-init → Config creation → Testing
- US3: Flag implementation → Scope detection → Validation → Testing

### Parallel Opportunities

**8 tasks can run in parallel**:
- Setup phase: 2 parallel tasks (T002-T003) - Directory creation
- Polish phase: 2 parallel tasks (T039-T040) - Documentation

**Sequential bottlenecks**:
- Phase 2 (Foundational) blocks all user stories
- US3 depends on US1 and US2 functionality existing

---

## Parallel Example: Setup Phase

```bash
# Launch parallel setup tasks together:
Task: "Create ram/storage/ directory for storage modules"
Task: "Create ram/storage/__init__.py to mark as package"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T008) - CRITICAL
3. Complete Phase 3: User Story 1 (T009-T018)
4. **STOP and VALIDATE**: Test local storage
   - Run `ram init` in test directory
   - Verify .ragged_memory/ created
   - Test isolation between projects
5. MVP complete - local storage working

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Local storage MVP! 🎯
3. Add User Story 2 → Test independently → Global storage working
4. Add User Story 3 → Test independently → Full scope control
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (local storage)
   - Developer B: User Story 2 (global storage)
   - Developer C: Prepares US3 (awaits US1/US2)
3. US3 starts after US1/US2 complete
4. Stories integrate naturally (share same base classes)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- No tests directory or test tasks (per Constitution: tests NOT required for prototypes)
- Manual validation through running commands and observing output
- Commit after completing each phase
- Stop at any checkpoint to validate story independently
- File paths are specific (not "create a file" but "create ram/storage/scope.py")
- Avoid: vague tasks, same file conflicts, unclear acceptance criteria

---

## Manual Validation Checkpoints

Since automated tests are not required (per Constitution), validate manually at these checkpoints:

**After Phase 2 (Foundational)**:
- All storage classes import without errors
- StorageScope enum has LOCAL and GLOBAL values
- Config loads defaults correctly
- ProjectContext detects project roots

**After Phase 3 (US1)**:
- `ram init` creates .ragged_memory/ directory
- Re-running `ram init` shows "already initialized"
- .ragged_memory/ contains LanceDB files
- Different projects have isolated stores

**After Phase 4 (US2)**:
- ~/.ragged_memory/ auto-creates on first access
- config.toml created with defaults
- Global store accessible from any directory
- Multiple directories access same global data

**After Phase 5 (US3)**:
- `--global` flag forces global scope
- `--local` flag forces local scope
- Conflicting flags show error
- Output indicates which scope is active
- Help shows scope flag documentation

**After Phase 6 (Polish)**:
- All classes have docstrings
- README documents scope usage
- Performance meets goals (<100ms detection, <500ms init)
- Edge cases handled gracefully
- Paths resolve correctly

---

## Success Criteria Mapping

Each user story maps to spec success criteria:

**US1 → SC-002**: Project-local information never leaks (0% cross-project leakage)
**US2 → SC-003**: Global information accessible from any directory (100% consistency)
**US3 → SC-001**: Users correctly choose scope (100% after reading help)
**US3 → SC-004**: Users understand active scope within 5 seconds
**All → SC-005**: Scope selection adds <2 seconds to workflow
**All → SC-006**: Zero data loss when switching scopes
