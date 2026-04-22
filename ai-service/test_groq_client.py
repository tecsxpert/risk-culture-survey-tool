import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from services.groq_client import groq_client

def test():
    print("\n===== GroqClient Test =====")
    print("Sending test message to Groq...\n")

    result = groq_client.chat(
        system_prompt="You are an assistant for a Risk Culture Survey Tool.",
        user_message="In one sentence, what is risk culture in an organisation?",
        temperature=0.3,
        max_tokens=100
    )

    print("\n===== Result =====")
    for key, value in result.items():
        print(f"{key:20}: {value}")
    print("==================")

    if result["is_fallback"]:
        print("\nDay 2 status: FAILED ✗ — check error above")
    else:
        print("\nDay 2 status: COMPLETE ✓")

if __name__ == "__main__":
    test()