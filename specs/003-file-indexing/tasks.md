# Tasks: File Indexing and Embedding

**Input**: Design documents from `/specs/003-file-indexing/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/, research.md, quickstart.md

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

**Purpose**: Project dependencies and basic structure for file indexing

- [x] T001 Update pyproject.toml with new dependencies (chonkie, sentence-transformers)
- [x] T002 [P] Create ram/indexing/ directory for indexing modules
- [x] T003 [P] Create ram/indexing/__init__.py to mark as package
- [x] T004 [P] Create ram/models/ directory for data models
- [x] T005 [P] Create ram/models/__init__.py to mark as package

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core indexing infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Create Chunk dataclass in ram/models/chunk.py with text, start_index, end_index, chunk_index attributes
- [x] T007 Create FileChunker class in ram/indexing/chunker.py with Chonkie SemanticChunker integration
- [x] T008 Implement chunk() method in FileChunker that uses Chonkie to split text into chunks
- [x] T009 Create EmbeddingGenerator class in ram/indexing/embedder.py with sentence-transformers integration
- [x] T010 Implement generate() method in EmbeddingGenerator that creates embeddings for chunks
- [x] T011 Create FileIndexer class in ram/indexing/indexer.py for orchestrating chunk → embed → store
- [x] T012 Extend MemoryStore in ram/storage/store.py to support storing chunks with metadata

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Basic File Indexing (Priority: P1) 🎯 MVP

**Goal**: Users can index UTF-8 text files into local storage and have content become searchable

**Independent Test**: Run `ram add document.txt` with a text file, verify chunks are stored in LanceDB, and confirm metadata is preserved

### Implementation for User Story 1

- [x] T013 [US1] Create ram/cli/commands/add.py module for add command
- [x] T014 [US1] Implement add command function with file path argument in ram/cli/commands/add.py
- [x] T015 [US1] Add file validation (exists, readable, UTF-8) in add command
- [x] T016 [US1] Add file size check (<10MB limit) in add command
- [x] T017 [US1] Implement read_file() helper that reads UTF-8 text in add command
- [x] T018 [US1] Integrate FileChunker to split file content in add command
- [x] T019 [US1] Integrate EmbeddingGenerator to create chunk embeddings in add command
- [x] T020 [US1] Create index entries (text + vector + metadata) in add command
- [x] T021 [US1] Store chunks in local LanceDB via MemoryStore in add command
- [x] T022 [US1] Add success/error messages with Rich formatting in add command
- [x] T023 [US1] Register add command with main app in ram/cli/app.py
- [x] T024 [US1] Test add command manually (ram add test.txt in test directory)
- [x] T025 [US1] Verify chunks stored in LanceDB with correct schema
- [x] T026 [US1] Test error handling (file not found, not UTF-8, too large)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently
- Running `ram add file.txt` indexes the file
- Chunks are stored in local LanceDB with metadata
- Error messages are clear and helpful

---

## Phase 4: User Story 2 - Intelligent Chunking (Priority: P2)

**Goal**: Handle large files by automatically chunking with semantic boundaries preserved

**Independent Test**: Index a large file (>10KB), verify it's split into multiple chunks, and confirm chunks maintain context

### Implementation for User Story 2

- [x] T027 [US2] Configure Chonkie SemanticChunker with chunk_size=512 and chunk_overlap=50 in FileChunker
- [x] T028 [US2] Add progress feedback for chunking large files (>1MB) in add command
- [x] T029 [US2] Implement batch embedding generation for efficiency in EmbeddingGenerator
- [x] T030 [US2] Add chunk position metadata (chunk_index) to index entries in add command
- [x] T031 [US2] Implement batch storage for large chunk sets in MemoryStore
- [x] T032 [US2] Add progress bar for embedding generation using Rich in add command
- [x] T033 [US2] Test with 100KB file to verify chunking produces multiple chunks
- [x] T034 [US2] Test with 1MB file to verify progress feedback works
- [x] T035 [US2] Verify chunks have sequential indices and preserve source positions

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently
- Small files index quickly without progress bars
- Large files show progress and chunk appropriately
- All chunks maintain reference to source file

---

## Phase 5: User Story 3 - Scope-Aware Indexing (Priority: P3)

**Goal**: Users can control whether files are indexed locally or globally using scope flags

**Independent Test**: Index a file with `--global` flag, navigate to different directories, and verify the indexed content is accessible globally

### Implementation for User Story 3

- [x] T036 [US3] Add scope detection logic to add command using ctx.obj for flag access
- [x] T037 [US3] Implement StorageManager integration for scope-based store selection in add command
- [x] T038 [US3] Handle --global flag to force global scope in add command
- [x] T039 [US3] Handle --local flag to force local scope in add command
- [x] T040 [US3] Add scope indicator to command output using format_scope_indicator() in add command
- [x] T041 [US3] Test indexing with --global flag (ram --global add file.txt)
- [x] T042 [US3] Test indexing with --local flag (ram --local add file.txt)
- [x] T043 [US3] Verify global scope accessible from multiple directories
- [x] T044 [US3] Verify local scope isolated per project

**Checkpoint**: All user stories should now be independently functional
- Scope flags work correctly
- Default scope detection works (local in projects, global elsewhere)
- Output clearly indicates active scope
- Chunks stored in correct LanceDB table

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T045 [P] Add comprehensive docstrings to all indexing classes
- [x] T046 [P] Update README.md with ram add documentation and examples
- [x] T047 Implement file hash calculation (SHA256) for duplicate detection in add command
- [x] T048 Add duplicate detection query to check if file already indexed in add command
- [x] T049 Add user prompt for re-indexing duplicates in add command
- [x] T050 Test duplicate detection (index same file twice)
- [x] T051 Test encoding error handling with non-UTF-8 file
- [x] T052 Test permission error handling with protected file
- [x] T053 Test file size limit with 11MB file
- [x] T054 Verify embedding model downloads and caches correctly on first run
- [x] T055 Test performance: 100KB file indexes in <5 seconds
- [x] T056 Validate LanceDB schema matches data-model.md specification
- [x] T057 Create example files demonstrating indexing usage in docs/examples/
- [x] T058 Verify metadata (file_path, chunk_index, timestamp) stored correctly

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1 (enhances chunking)
- **User Story 3 (P3)**: Depends on US1 being complete (adds scope control to existing indexing)

### Within Each User Story

- Foundational classes must exist before any user story (Phase 2 gates all)
- US1: File validation → Chunking → Embedding → Storage → Testing
- US2: Configure chunker → Progress feedback → Batch processing → Testing
- US3: Scope detection → Store selection → Output formatting → Testing

### Parallel Opportunities

**5 tasks can run in parallel**:
- Setup phase: 4 parallel tasks (T002-T005) - Directory creation
- Polish phase: 2 parallel tasks (T045-T046) - Documentation

**Sequential bottlenecks**:
- Phase 2 (Foundational) blocks all user stories
- US3 depends on US1 functionality existing

---

## Parallel Example: Setup Phase

```bash
# Launch parallel setup tasks together:
Task: "Create ram/indexing/ directory for indexing modules"
Task: "Create ram/indexing/__init__.py to mark as package"
Task: "Create ram/models/ directory for data models"
Task: "Create ram/models/__init__.py to mark as package"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T012) - CRITICAL
3. Complete Phase 3: User Story 1 (T013-T026)
4. **STOP and VALIDATE**: Test file indexing
   - Run `ram add test.txt` in test directory
   - Verify chunks created and stored in LanceDB
   - Test error handling (bad file, encoding, size)
5. MVP complete - basic file indexing working

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Basic indexing MVP! 🎯
3. Add User Story 2 → Test independently → Large file support working
4. Add User Story 3 → Test independently → Full scope control
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (basic indexing)
   - Developer B: User Story 2 (chunking enhancements)
   - Developer C: Prepares US3 (awaits US1)
3. US3 starts after US1 complete
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
- File paths are specific (not "create a file" but "create ram/indexing/chunker.py")
- Avoid: vague tasks, same file conflicts, unclear acceptance criteria

---

## Manual Validation Checkpoints

Since automated tests are not required (per Constitution), validate manually at these checkpoints:

**After Phase 2 (Foundational)**:
- All indexing classes import without errors
- Chunk dataclass has required attributes
- FileChunker can split sample text
- EmbeddingGenerator creates 384-dim vectors
- MemoryStore can store chunks with metadata

**After Phase 3 (US1)**:
- `ram add document.txt` successfully indexes file
- Chunks stored in LanceDB with correct schema
- File metadata (path, hash, timestamp) preserved
- Error messages clear for invalid files
- UTF-8 validation works correctly

**After Phase 4 (US2)**:
- Large files (>10KB) chunk appropriately
- Progress feedback shows for large files
- Batch processing handles thousands of chunks
- Chunk indices preserve source order
- Semantic boundaries respected in splits

**After Phase 5 (US3)**:
- `--global` flag stores in global LanceDB
- `--local` flag stores in local LanceDB
- Default scope detection works correctly
- Output indicates active scope
- Scope isolation verified (local != global)

**After Phase 6 (Polish)**:
- All classes have docstrings
- README documents ram add usage
- Duplicate detection prevents re-indexing
- Performance meets targets (<5s for 100KB)
- Edge cases handled gracefully

---

## Success Criteria Mapping

Each user story maps to spec success criteria:

**US1 → SC-001**: Users can index a text file in under 5 seconds for files up to 100KB
**US1 → SC-004**: Users receive clear feedback on indexing status within 1 second
**US1 → SC-005**: The system handles at least 10 file types without errors
**US2 → SC-002**: Indexed file content is findable through semantic search with 95% relevance
**US2 → SC-003**: Chunking preserves context such that search results remain coherent
**US2 → SC-006**: Zero data loss occurs during chunking and embedding process
**US3 → SC-007**: Scope selection correctly isolates indexed content 100% of the time
