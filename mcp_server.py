import os

# Disable telemetry
os.environ["ANONYMIZED_TELEMETRY"] = "False"

# Neutralize posthog before any imports that might use it
import posthog
posthog.capture = lambda *args, **kwargs: None

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
        }
    }
}

# Set env vars for anthropic (z.ai)
if token := os.getenv("ANTHROPIC_AUTH_TOKEN"):
    os.environ["ANTHROPIC_API_KEY"] = token
os.environ["ANTHROPIC_BASE_URL"] = "https://api.z.ai/api/anthropic"

memory = Memory.from_config(config)

@mcp.tool()
def add_memory(content: str, user_id: str = "local-user"):
    """
    CRITICAL: Permanent storage for project rules, architectural decisions, 
    user preferences, and unique technical constraints. 
    Use this to save any specific logic or facts that should persist across 
    future turns and sessions, ensuring they are not lost when the 
    conversation context is cleared.
    """
    memory.add(content, user_id=user_id)
    return f"Memory stored for {user_id}"

@mcp.tool()
def search_memories(query: str, user_id: str = "local-user"):
    """
    MANDATORY: Semantic search across the long-term knowledge base. 
    Call this tool immediately if the user refers to specific project 
    details, prior decisions, or terminology that you do not recognize 
    from your internal training data. 
    It retrieves the necessary context to ensure responses are grounded in 
    established facts.
    """
    results = memory.search(query, user_id=user_id)
    return results

if __name__ == "__main__":
    mcp.run(transport="stdio")