"""
AI-Powered Student Assistant

Uses Claude claude-opus-4-5, the most capable model in the Claude family (and among the
smartest models available: GPT-4, Claude Sonnet, Claude Opus).

Model comparison:
  - GPT-4 (OpenAI): Very capable general-purpose model
  - Claude Sonnet (Anthropic): Fast, balanced capability and speed
  - Claude Opus (Anthropic): Most intelligent, best for complex reasoning tasks ✓

Claude claude-opus-4-5 is chosen here because it offers the highest intelligence and
reasoning ability, making it ideal for helping students with complex academic tasks.
"""

import os
from anthropic import Anthropic, APIConnectionError, APIError, AuthenticationError, RateLimitError

MODEL = "claude-opus-4-5"  # Smartest model: Opus > Sonnet > GPT in reasoning tasks

SYSTEM_PROMPT = """You are an expert AI-powered student assistant. Your role is to help
students understand difficult concepts, solve problems, and learn effectively across all
academic subjects including mathematics, science, history, literature, and more.

Guidelines:
- Explain concepts clearly and at an appropriate level for the student
- Break down complex problems into manageable steps
- Encourage critical thinking rather than just providing answers
- Provide examples and analogies to aid understanding
- Be patient, supportive, and encouraging
"""


def run_assistant() -> None:
    """Run the interactive student assistant."""
    try:
        client = Anthropic()
    except AuthenticationError:
        print("Error: Invalid or expired ANTHROPIC_API_KEY.")
        raise SystemExit(1)

    conversation_history: list[dict] = []

    print("=" * 60)
    print("  AI-Powered Student Assistant (powered by Claude Opus)")
    print("  The smartest model for complex academic tasks")
    print("=" * 60)
    print("Type your question or 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye! Keep learning!")
            break

        conversation_history.append({"role": "user", "content": user_input})

        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=conversation_history,
            )
        except AuthenticationError:
            print("Error: Invalid or expired API key. Please check ANTHROPIC_API_KEY.")
            raise SystemExit(1)
        except RateLimitError:
            print("Error: Rate limit reached. Please wait a moment and try again.")
            conversation_history.pop()
            continue
        except APIConnectionError:
            print("Error: Could not connect to the API. Check your internet connection.")
            conversation_history.pop()
            continue
        except APIError as exc:
            print(f"Error: API error occurred ({exc}). Please try again.")
            conversation_history.pop()
            continue

        assistant_message = response.content[0].text
        conversation_history.append(
            {"role": "assistant", "content": assistant_message}
        )

        print(f"\nAssistant: {assistant_message}\n")


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: Please set the ANTHROPIC_API_KEY environment variable.")
        raise SystemExit(1)
    run_assistant()
