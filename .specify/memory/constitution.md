<!--
  Sync Impact Report
  ==================
  Version: 1.0.0 → 1.1.0
  Change Type: MINOR (Expanded guidance on testing)
  Date: 2026-02-14

  Modified Principles:
  - EXPANDED: II. No Over-Engineering (added explicit "no tests" requirement)

  Modified Sections:
  - Development Guidelines: Added "Testing Policy" subsection
  - Quality Standards: Expanded "What Doesn't Matter" to explicitly exclude tests

  Templates Requiring Updates:
  ✅ .specify/templates/tasks-template.md (Updated test sections to reference Constitution default)
  ✅ .specify/templates/plan-template.md (Constitution Check section references this file)
  ✅ .specify/templates/spec-template.md (No changes needed - already compatible)

  Follow-up TODOs:
  - None (all templates aligned with constitution)
-->

# Ragged Memory Constitution

## Core Principles

### I. Prototype Simplicity

This is a basic prototype project. All implementations MUST prioritize minimal viable functionality over completeness. Features should demonstrate core concepts without attempting production-grade robustness. Every component should answer "what is the simplest thing that could work?" before implementation.

**Rationale**: Prototypes exist to validate ideas quickly. Premature optimization or production-level infrastructure slows learning and iteration.

### II. No Over-Engineering

Error trapping and defensive programming are EXPLICITLY PROHIBITED unless absolutely necessary for demonstrating core functionality. Avoid abstractions, design patterns, or architectural complexity beyond immediate needs. Do not build for hypothetical future requirements.

**Tests are NOT required** for prototypes. No unit tests, integration tests, contract tests, or any automated testing infrastructure. Manual validation through running the code is sufficient. Test-driven development (TDD) is explicitly NOT practiced for prototypes.

**Rationale**: Over-engineering obscures the prototype's purpose and wastes effort on features that may never be needed. Simple, direct code is faster to write and easier to validate or discard. Tests add overhead without value during rapid prototyping.

### III. Code Clarity

All code MUST be clean, idiomatic, tidy, simple, and easy to grok. Use language-standard conventions. Favor explicitness over cleverness. Code should be self-documenting through clear naming and straightforward logic. Minimize cognitive load for readers.

**Rationale**: Prototypes are exploratory. Code that's hard to understand slows iteration and makes it difficult to share learnings with others.

### IV. File Organization

One class per file. MUST follow single-responsibility file structure. File names MUST match the primary class/component they contain. No multi-class files except where language conventions explicitly require it (e.g., tightly coupled private helpers).

**Rationale**: Clear file boundaries make code navigation trivial and reduce merge conflicts during rapid iteration.

## Development Guidelines

### Code Structure

- Keep file sizes small (prefer < 200 lines)
- Use meaningful names that reveal intent
- Avoid nesting beyond 3 levels deep
- Remove dead code immediately - don't comment it out

### Implementation Approach

- Start with the simplest possible implementation
- Only add complexity when current approach demonstrably fails
- Delete code aggressively when requirements change
- Prefer duplication over premature abstraction (DRY is not a goal for prototypes)

### Documentation

- Code should be self-explanatory through naming and structure
- Add comments only for non-obvious decisions or constraints
- Maintain a simple README with setup instructions
- Document architectural decisions in commit messages if relevant

### Testing Policy

**Tests are NOT required for prototypes.** This includes:
- No unit tests
- No integration tests
- No contract tests
- No end-to-end tests
- No test infrastructure or frameworks
- No TDD (Test-Driven Development)

**Validation approach**: Run the code manually and verify it works. If it breaks, fix it directly. Speed of iteration matters more than test coverage.

## Quality Standards

### What Matters

- **Correctness**: Code does what it claims to do
- **Clarity**: Another developer can understand it in < 5 minutes
- **Completeness**: Demonstrates the intended concept fully

### What Doesn't Matter (For This Prototype)

- **Tests** (unit, integration, contract, end-to-end, or any automated testing)
- **Test infrastructure** (frameworks, runners, coverage tools)
- Error handling beyond crash-and-fix
- Performance optimization
- Security hardening
- Scalability planning
- Production deployment concerns

### Code Review Focus

When reviewing code, check:

1. Does it follow prototype simplicity? (No unnecessary complexity?)
2. Is it minimal and clean?
3. One class per file?
4. Easy to understand?

If yes to all four, approve. If no, request simplification.

## Governance

### Authority

This constitution supersedes all other development practices, style guides, or architectural preferences for this project. When in doubt, refer to the four core principles.

### Amendments

1. Amendments must be proposed with clear rationale
2. Amendment requires documenting version bump and change log
3. All active feature branches must be notified of constitutional changes

### Compliance

- All code reviews MUST verify constitutional compliance
- Any complexity beyond prototype needs MUST be explicitly justified
- Unjustified complexity is grounds for rejecting a PR
- When constitution conflicts with external guidelines (e.g., language best practices), constitution wins unless it creates demonstrable harm

### Version Tracking

Changes to this constitution MUST follow semantic versioning:
- **MAJOR**: Principle removal, redefinition, or scope changes that invalidate prior work
- **MINOR**: New principle addition or expanded guidance
- **PATCH**: Clarifications, wording improvements, typo fixes

**Version**: 1.1.0 | **Ratified**: 2026-02-14 | **Last Amended**: 2026-02-14
