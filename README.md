# mem0-server

A Model Context Protocol (MCP) server providing long-term memory storage and semantic search capabilities using Mem0 with local embeddings.

## Overview

This server exposes two MCP tools for persistent memory management:
- **add_memory** - Store facts, project rules, architectural decisions, and preferences
- **search_memories** - Semantic search across stored memories

## Architecture

| Component | Provider | Configuration |
|-----------|----------|---------------|
| Vector Store | Chroma | Local storage at `~/mem0-server/chroma_data` |
| Embeddings | Ollama | `nomic-embed-text` model on `localhost:11434` |
| LLM | Anthropic | `glm-4.7` via z.ai proxy |

## Installation

```bash
# Using uv (recommended)
uv sync

# Or with pip
pip install -e .
```

## Prerequisites

### Nix Users

This project uses `shell.nix` with `direnv` for development. The shell configuration provides `libstdc++.so.6` which NumPy requires.

```bash
# Install direnv if needed
nix-env -iA nixpkgs.direnv

# Allow the .envrc
direnv allow

# Or enter nix-shell directly
nix-shell
```

**Note:** Devbox was attempted but did not work for this project's requirements.

> [!WARNING]
> Never set `LD_LIBRARY_PATH` globally (e.g., in `~/.bashrc`, `~/.profile`, or home-manager `sessionVariables`). This will break GDM and prevent login. The `shell.nix` approach scopes the variable to this project only.

1. **Ollama** - Install and run the Ollama service with nomic-embed-text:

   Using systemd:
   ```bash
   # Check if ollama service is running
   systemctl status ollama

   # Start ollama service
   systemctl start ollama
   systemctl enable ollama  # Start on boot

   # Pull the embedding model
   ollama pull nomic-embed-text
   ```

   Or run directly:
   ```bash
   ollama serve
   ollama pull nomic-embed-text
   ```

2. **Anthropic API Token** - Set your authentication token:
   ```bash
   export ANTHROPIC_AUTH_TOKEN="your_token_here"
   ```

## Usage

### Running the Server

```bash
uv run --directory /path/to/mem0-server python mcp_server.py
```

Or via MCP client configuration (e.g., in Claude Code):
```json
{
  "mcpServers": {
    "mem0-local": {
      "command": "/path/to/mem0-server/.venv/bin/python",
      "args": [
        "/path/to/mem0-server/mcp_server.py"
      ],
      "env": {
        "MEM0_USER_ID": "local-user",
        "MEM0_EMBEDDING_PROVIDER": "ollama",
        "MEM0_EMBEDDING_MODEL": "nomic-embed-text",
        "OLLAMA_BASE_URL": "http://localhost:11434",
        "MEM0_VECTOR_STORE": "chroma",
        "CHROMA_DB_PATH": "/path/to/mem0-server/chroma_data"
      },
      "toolConfig": {
        "add_memory": "auto",
        "search_memories": "auto"
      }
    }
  }
}
```

> [!NOTE]
> Both `toolConfig.auto` (server-side, FastMCP-only) and `permissions.allow` (client-side, any MCP server) work for auto-approving tools. Use `permissions.allow` with `mcp__mem0-server__*` pattern as an alternative.

### Testing

```bash
# Run the test script
uv run --directory /path/to/mem0-server python test_mem0_mcp.py

# Or test add_memory directly
uv run --directory /path/to/mem0-server python -c "from mcp_server import add_memory; print(add_memory('The project password is Alpha-99'))"
```

## MCP Tools

### `add_memory(content: str, user_id: str = "local-user")`

Permanently stores information that should persist across sessions.

**Use for:**
- Project rules and architectural decisions
- User preferences and configurations
- Unique technical constraints
- Domain-specific knowledge

### `search_memories(query: str, user_id: str = "local-user")`

Performs semantic search across stored memories.

**Use when:**
- User refers to project-specific details not in training data
- Context is needed about prior decisions
- Looking up established facts or preferences

## Claude Code Permissions

To enable these memory tools in Claude Code, add the following permission configuration:

```json
{
  "permissions": {
    "allow": [
      "mcp__mem0-server__add_memory",
      "mcp__mem0-server__search_memories"
    ]
  }
}
```

This allows Claude to use both the `add_memory` and `search_memories` tools without requiring permission prompts.

## Features

- **Privacy-First**: All data stored locally in ChromaDB
- **No Telemetry**: PostHog telemetry disabled by default
- **Semantic Search**: Vector-based retrieval using Ollama embeddings
- **Session-Persistent**: Memories survive context clears and session restarts


  