# Feature Specification: Dual Storage Scopes

**Feature Branch**: `002-storage-scopes`
**Created**: 2026-02-14
**Status**: Draft
**Input**: User description: "a memory can be either local to the directory or global for the user, in both cases memories are stored on disk"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Project-Local Memory Storage (Priority: P1)

Users need to store information that is specific to the project they're working on. This information should only be accessible when working within that project directory, not in other projects or locations.

**Why this priority**: Project-specific knowledge is the primary use case for RAM. Without this, users cannot maintain separate contexts for different codebases.

**Independent Test**: Can be fully tested by storing information in one project directory, verifying it's accessible within that project, and confirming it's not visible from other directories.

**Acceptance Scenarios**:

1. **Given** a user is in a project directory, **When** they store information without specifying a scope, **Then** the information is saved as project-local by default
2. **Given** a user has stored project-local information, **When** they query from the same project directory, **Then** they can retrieve that information
3. **Given** a user has stored project-local information in Project A, **When** they query from Project B, **Then** Project A's information is not visible
4. **Given** multiple users working on the same project, **When** one user stores project-local information, **Then** other users with access to the project can retrieve it

---

### User Story 2 - User-Global Memory Storage (Priority: P2)

Users need to store personal knowledge that applies across all their projects and should be accessible regardless of which directory they're working in.

**Why this priority**: Personal knowledge base functionality is essential but secondary to project context. Users first need project isolation, then cross-project accessibility.

**Independent Test**: Can be tested by storing information globally, navigating to different directories, and verifying the information is accessible everywhere.

**Acceptance Scenarios**:

1. **Given** a user explicitly chooses global scope, **When** they store information, **Then** the information is saved as user-global
2. **Given** a user has stored global information, **When** they query from any directory, **Then** they can retrieve that information
3. **Given** multiple users on the same machine, **When** User A stores global information, **Then** User B cannot access User A's global information
4. **Given** a user has both project-local and global information, **When** they query, **Then** they can choose to search only global, only local, or both scopes

---

### User Story 3 - Scope Selection Control (Priority: P3)

Users need to explicitly control which storage scope to use when storing or searching information. They should understand which scope they're operating in and easily switch between scopes.

**Why this priority**: While defaults work for most cases, power users need explicit control. This prevents accidental storage in the wrong scope.

**Independent Test**: Can be tested by storing and searching with explicit scope flags and verifying correct scope selection.

**Acceptance Scenarios**:

1. **Given** a user wants to force global scope, **When** they specify the global flag, **Then** information is stored/searched in global scope regardless of location
2. **Given** a user wants to force project scope, **When** they specify the project flag, **Then** information is stored/searched in project scope even if no project detected
3. **Given** a user executes a command, **When** they view output, **Then** the system indicates which scope was used (project name or "global")
4. **Given** a user is unsure which scope to use, **When** they view help, **Then** they see clear guidance on when to use each scope

---

### Edge Cases

- What happens when a user stores project-local information in a directory that isn't a project root?
- How does the system handle a project that's moved to a different location on disk?
- What happens when a user accidentally stores personal information in project scope?
- How does the system behave when storage locations aren't writable?
- What happens if both project and global stores contain similar information?
- How does the system identify what qualifies as a "project directory"?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support two distinct storage scopes: project-local and user-global
- **FR-002**: System MUST use project-local scope as the default when operating within a project directory
- **FR-003**: System MUST persist project-local information such that it's accessible only from within that project
- **FR-004**: System MUST persist user-global information such that it's accessible from any location
- **FR-005**: System MUST provide a mechanism for users to explicitly select global scope
- **FR-006**: System MUST provide a mechanism for users to explicitly select project scope
- **FR-007**: System MUST isolate global stores between different users on the same machine
- **FR-008**: System MUST allow querying within a single scope (project-only or global-only)
- **FR-009**: System MUST allow querying across both scopes simultaneously when desired
- **FR-010**: System MUST indicate which scope was used in operation results
- **FR-011**: System MUST maintain data integrity such that information in one scope cannot corrupt another scope
- **FR-012**: System MUST preserve stored information persistently across system restarts

### Key Entities

- **Memory Store**: A persistent collection of stored information. Has a scope (project or global), a location on disk, and contains memory entries.
- **Scope**: Defines the visibility boundary for stored information. Either "project" (local to directory) or "global" (user-wide).
- **Project Context**: The current project directory that defines the active project-local store. Determined by directory location.
- **Storage Location**: Physical location where memories are persisted. Project stores are within project directories, global stores are in user home directory.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can correctly choose appropriate scope (project vs global) in 100% of scenarios after reading help documentation
- **SC-002**: Project-local information is never accidentally visible from other projects (0% cross-project leakage)
- **SC-003**: Global information is accessible from any directory with 100% consistency
- **SC-004**: Users understand which scope they're operating in within 5 seconds of viewing command output
- **SC-005**: Storage scope selection adds less than 2 seconds to user workflow
- **SC-006**: Zero data loss when switching between scopes or projects

### Assumptions

- Users understand the concept of "local to this project" vs "global to me"
- Users work with multiple projects simultaneously or over time
- Project directories remain relatively stable (not constantly moved/renamed)
- Users want project isolation by default (don't want all information mixed)
- The system can reliably identify project boundaries (e.g., via git root, markers)

### Dependencies

- **001-cli-scaffolding**: Requires CLI infrastructure to accept scope flags and arguments

### Scope

**In Scope**:
- Two storage scopes: project-local and user-global
- Persistent storage to disk for both scopes
- Scope selection mechanism (default + explicit flags)
- Isolation between scopes
- Indication of active scope in outputs
- User-level isolation for global stores

**Out of Scope**:
- Team-shared storage (future consideration)
- Cloud synchronization (future consideration)
- Fine-grained permissions within scopes (future consideration)
- Automatic scope detection beyond project boundaries (future consideration)
- Migration tools between scopes (future consideration)
- Scope analytics or usage tracking (future consideration)
- Multiple simultaneous project scopes (user can only be in one project at a time)
