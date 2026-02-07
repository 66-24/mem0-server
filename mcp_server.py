import os
from mcp.server.fastmcp import FastMCP
from mem0 import Memory

# Initialize FastMCP server
mcp = FastMCP("Mem0-Local")

# Initialize Local Mem0 with your specific config
# Note: This matches your logic for Ollama + Chroma
config = {
    "vector_store": {
        "provider": "chroma",
        "config": {
            "path": os.path.expanduser("~/mem0-server/chroma_data"),
        }
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text",
            "ollama_base_url": "http://localhost:11434",
        }
    },
    "llm": {
        "provider": "anthropic",
        "config": {
            "model": "glm-4.7",
            "api_key": os.getenv("ANTHROPIC_AUTH_TOKEN"),
        }
    }
}

# Set env var for anthropic base URL (z.ai)
os.environ["ANTHROPIC_BASE_URL"] = "https://api.z.ai/api/anthropic"

memory = Memory.from_config(config)

@mcp.tool()
def add_memory(content: str, user_id: str = "local-user"):
    """Store a new piece of information in long-term memory."""
    memory.add(content, user_id=user_id)
    return f"Memory stored for {user_id}"

@mcp.tool()
def search_memories(query: str, user_id: str = "local-user"):
    """Search for relevant past information."""
    results = memory.search(query, user_id=user_id)
    return results

if __name__ == "__main__":
    mcp.run(transport="stdio")