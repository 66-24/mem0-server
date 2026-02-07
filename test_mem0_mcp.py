from mcp_server import add_memory, search_memories

# Test Writing
print("Testing Add...")
print(add_memory("HelmNet uses a TPU-optimized backend."))

# Test Reading
print("\nTesting Search...")
print(search_memories("What backend does HelmNet use?"))