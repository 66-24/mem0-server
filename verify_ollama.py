#!/usr/bin/env -S uv run --script

# /// script
# dependencies = ["requests"]
# ///

import requests
import sys

def check_connection():
    """Checks if Ollama is running and has the specific model."""
    try:
        print("   ...Connecting to Ollama...")
        r = requests.get("http://localhost:11434/api/tags", timeout=5)

        if r.status_code != 200:
            print(f"   ❌ Ollama returned status {r.status_code}")
            return False

        models = [m['name'] for m in r.json().get('models', [])]

        # Check for model (handles tags like :latest)
        found = any("nomic-embed-text" in m for m in models)

        if found:
            print("   ✅ Ollama running. Model 'nomic-embed-text' found.")
            return True
        else:
            print(f"   ❌ Model 'nomic-embed-text' missing. Found: {models}")
            print("   👉 Run: ollama pull nomic-embed-text")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Could not connect to Ollama (Connection Refused). Is it running?")
        return False
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return False

def check_embedding():
    """Checks if the embedding endpoint actually works."""
    try:
        print("   ...Testing Embedding Endpoint...")

        # Payload must be defined for the POST request
        payload = {
            "model": "nomic-embed-text",
            "input": "Sanity check"
        }

        r = requests.post("http://127.0.0.1:11434/api/embed",
                  json=payload,
                  timeout=5)

        if r.ok:
            print("   ✅ Embeddings endpoint working.")
            return True

        print(f"   ❌ Unexpected response (status {r.status_code}): {r.text[:200]}")
        return False
    except Exception as e:
        print(f"   ❌ Embedding check failed: {e}")
        return False

# Execution Flow
print("🔍 Starting Verification...")
if check_connection():
    if check_embedding():
        sys.exit(0)
    else:
        sys.exit(1)
else:
    sys.exit(1)
