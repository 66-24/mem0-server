# MCP Mem0 Integration - Memory-First Workflow

## CRITICAL: You Have Persistent Memory

Claude has MCP Server mem0 server configured. Memory survives context clears. Use it.

---

## MANDATE: Search Memory Before Acting

**ALWAYS search memory FIRST when:**
- Interpreting any user preference or requirement
- Making architectural or implementation decisions
- Applying coding style or patterns
- Running git operations (commits, branches)
- Encountering project-specific terminology

**How to search:**
```
Query: "What are the user's preferences for X?"
Query: "How does this project handle Y?"
```

**If empty:** State "No existing context in memory" - then proceed.

---

## MANDATE: Add to Memory After Learning

**ALWAYS add to memory after:**
- User states a preference (coding style, workflows, dislikes)
- You make an architectural decision
- You discover project patterns/conventions
- You resolve confusing terminology
- Any insight useful for future sessions

**Store as atomic facts:**
- "User prefers minimal commits without Claude signatures"
- "Project uses FastAPI with lifetime dependency injection"
- "API routes follow /api/v1/{resource} pattern"

---

## Memory Tools

- `mcp__mem0-server__search_memories` - Semantic search
- `mcp__mem0-server__add_memory` - Store information

---

## Be Explicit About Memory Usage

Tell the user when you're using stored context:
- "Found in memory: you prefer X"
- "Adding to memory: Y pattern"

Build context over time. Each session enriches the memory store.
