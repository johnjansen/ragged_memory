# Ragged Memory (RAM)

> Lightweight semantic memory for LLMs at the command line

## What is RAM?

Ragged Memory (RAM) is a CLI tool that gives LLMs and their users a simple, persistent memory. Store information once, retrieve it later by meaning—not by remembering exact keywords. No complex setup, no external services, just a command-line tool that works.

**Core idea**: Your LLM conversations should remember what matters, both within a project and across your entire workflow.

## The Problem

**LLMs forget everything between conversations.** Every new chat starts from zero.

When working with AI assistants like Claude, ChatGPT, or local models:

- You constantly re-explain project conventions and decisions
- You copy-paste the same context into multiple conversations
- You lose valuable insights that came up in previous sessions
- Each AI interaction is isolated, with no shared knowledge

**Current solutions are too complex.** Vector databases and semantic search tools exist, but they require:
- Setting up servers or Docker containers
- Managing API keys and external services
- Learning complex query languages
- Significant infrastructure overhead

**What we need**: A dead-simple way to store and retrieve contextual information that both humans and LLMs can use trivially.

## The Solution

RAM provides **semantic memory via the command line**—simple enough for anyone to use, powerful enough to transform how you work with LLMs.

### Two Memory Scopes

**Project Memory** - Context specific to a codebase:
- "We use PostgreSQL with Prisma ORM"
- "API keys go in .env.local, never commit them"
- "Our CSS uses Tailwind with the custom theme in tailwind.config.js"

**Global Memory** - Personal knowledge that travels with you:
- "I prefer functional programming over OOP when possible"
- "My Git workflow: feature branches, squash commits before merge"
- "Python logging setup I always use: structlog with JSON output"

### Semantic Search

Find information by **meaning**, not memorization:

```
Stored: "Our authentication uses JWT tokens with 24-hour expiry"

Search: "How do we handle login?"
→ Found: "Our authentication uses JWT tokens..."

Search: "token lifespan"
→ Found: "Our authentication uses JWT tokens with 24-hour expiry"
```

No exact keyword matching required. Ask naturally, get relevant results.

## Use Cases

### Developers: Persistent Project Context

**Stop re-explaining your codebase to AI assistants.**

Store once: "Our backend is FastAPI, frontend is Next.js, deployed on Vercel"

Every new AI conversation can query this context instead of you repeating it.

**Build a personal knowledge base that grows with you.**

Capture useful patterns, configuration snippets, and hard-won insights. Retrieve them in any project, any time.

### LLM Tools: Augmented Memory

**Give AI assistants persistent memory.**

Tools like Claude, ChatGPT, and custom AI agents can store and retrieve information across conversations:
- User preferences ("I like TypeScript, avoid classes")
- Project patterns ("Use dependency injection via constructor")
- Team conventions ("All PRs need 2 approvals")

**Enable project-aware AI.**

Instead of generic responses, AI tools can query project memory and give contextually appropriate answers.

### Teams: Shared Tribal Knowledge

**Centralize the unwritten rules.**

Every team has knowledge that lives in people's heads:
- "Why did we choose this architecture?"
- "What's the deployment process?"
- "How do we structure tests?"

Store it in RAM. New team members can discover it. AI tools can reference it.

## Why This Matters

### For Individual Developers

**Reduce cognitive load.** Stop trying to remember every project detail. Store it, search it semantically.

**Faster onboarding.** Jump back into old projects by querying what you knew before.

**Compound learning.** Build a knowledge base that grows more valuable over time.

### For AI Workflows

**Break the amnesia barrier.** LLMs are incredibly capable but have zero memory between conversations. RAM bridges that gap.

**Context without copy-paste.** Stop manually injecting the same context into every conversation.

**Smarter AI interactions.** When an LLM can query relevant context on-demand, the quality of responses improves dramatically.

### For Teams

**Onboarding acceleration.** New developers can query "How do we...?" and get answers from stored team knowledge.

**Consistency.** AI tools and humans both reference the same source of truth.

**Living documentation.** Instead of docs that go stale, store knowledge incrementally as you work.

## Core Principles

RAM is designed around these beliefs:

**Simplicity First**
- Command-line interface, no GUIs or web apps
- Works immediately, no configuration required
- Store and search—that's it

**Semantic, Not Syntactic**
- Search by meaning, not keywords
- Natural language queries
- Forgiving retrieval (close enough is good enough)

**Local & Private**
- Runs on your machine
- No external services
- Your data stays yours

**Human & Machine**
- Easy for developers to use directly
- Easy for AI tools to integrate
- Structured output for programmatic use

**Scoped Appropriately**
- Project memory for codebase-specific knowledge
- Global memory for personal cross-project knowledge
- Clear boundaries, no confusion

## What Success Looks Like

**For individual use:**
- You naturally store useful information as you work
- You search RAM before searching Google/StackOverflow
- You reference RAM in every AI conversation

**For AI integration:**
- LLM tools automatically query RAM for context
- AI responses are consistently project-aware
- AI remembers your preferences and patterns

**For teams:**
- New developers ask RAM before asking people
- Team conventions are stored, not just spoken
- Institutional knowledge persists beyond individual memory

## What This Is Not

**Not a documentation replacement.** RAM complements docs, doesn't replace them. Use it for contextual snippets and patterns, not comprehensive reference material.

**Not a vector database.** Those are powerful but complex. RAM is deliberately simpler—good enough for most needs, trivial to use.

**Not production infrastructure.** This is a developer tool for local use, not a service you deploy.

**Not a knowledge graph.** No complex relationships or ontologies. Just store text, search by meaning.

## Open Questions

These are product decisions we need to make:

**Scope & Discovery:**
- Should RAM auto-index certain files (like `ARCHITECTURE.md` or `CONVENTIONS.md`)?
- How do users discover what's already stored?
- Should we show "related" results even when not searching?

**Storage & Organization:**
- Are two scopes (project + global) enough, or do we need more (e.g., team, client)?
- Should entries have tags/categories, or is semantic search sufficient?
- How do users manage/curate stored information over time?

**AI Integration:**
- How should LLM tools authenticate/authorize access?
- Should RAM provide a standard protocol/API for AI tools?
- How do we prevent AI tools from polluting the store with bad data?

**Sharing & Collaboration:**
- Should project memory be git-committable and shareable?
- How do teams sync global knowledge?
- What's the export/import story?

**Query Experience:**
- Should RAM suggest queries based on current context?
- How do users know if their query succeeded or failed?
- What's the feedback loop for improving search relevance?

## Status

**This is a product brief.** We're defining what to build and why it matters before diving into how to build it.

**Next step**: Validate assumptions with potential users, then spec the MVP.

---

**Feedback wanted:** Does this solve a real problem for you? What's missing? What's wrong?
