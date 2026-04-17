from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List

from huggingface_hub import InferenceClient

DEFAULT_MODEL = os.getenv("HF_MODEL", "openai/gpt-oss-120b")
MAX_TURNS_IN_MEMORY = int(os.getenv("MAX_TURNS_IN_MEMORY", "8"))


def load_system_prompt(path: str = "system_prompt.txt") -> str:
    prompt_path = Path(path)
    if not prompt_path.exists():
        # missing file flag - added this just in case one of us forgets to add
        # the prompt file on the same folder as the code
        raise FileNotFoundError(
            f"Could not find {path}. Put system_prompt.txt in the same folder as app.py."
        )
    return prompt_path.read_text(encoding="utf-8").strip()


def build_client() -> InferenceClient:
    token = os.getenv("HF_TOKEN")
    # missing token flag 
    if not token:
        raise EnvironmentError(
            "Missing HF_TOKEN environment variable. "
            "Create a Hugging Face token, then set it before running the app."
        )
    return InferenceClient(api_key=token)


def make_message(role: str, content: str) -> Dict[str, str]:
    return {"role": role, "content": content}


class ShakespeareChatbot:
    def __init__(self, system_prompt: str, model: str = DEFAULT_MODEL) -> None:
        self.system_prompt = system_prompt
        self.model = model
        self.client = build_client()
        self.history: List[Dict[str, str]] = []

    def _recent_history(self) -> List[Dict[str, str]]:
        limit = MAX_TURNS_IN_MEMORY * 2
        return self.history[-limit:]

    def _build_messages(self, user_input: str) -> List[Dict[str, str]]:
        messages: List[Dict[str, str]] = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self._recent_history())
        messages.append({"role": "user", "content": user_input})
        return messages

    def ask(self, user_input: str) -> str:
        messages = self._build_messages(user_input)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.85,
            max_tokens=220,
        )

        reply = response.choices[0].message.content.strip()
        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def clear_memory(self) -> None:
        self.history.clear()


def print_help() -> None:
    print(
        """
Commands:
  /help    Show commands
  /clear   Clear conversation memory
  /history Show saved turns
  /quit    Exit the chatbot
        """.strip()
    )


def print_history(bot: ShakespeareChatbot) -> None:
    if not bot.history:
        print("\nNo conversation history yet.\n")
        return

    print("\nSaved conversation:\n")
    for msg in bot.history:
        speaker = "You" if msg["role"] == "user" else "Shakespeare"
        print(f"{speaker}: {msg['content']}\n")


def run_cli() -> None:
    system_prompt = load_system_prompt()
    bot = ShakespeareChatbot(system_prompt=system_prompt)

    print("~" * 60)
    print("Shakespeare Chatbot")
    print("~" * 60)
    print(f"Model: {bot.model}")
    print("Type /help for commands.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nFare thee well.")
            break

        if not user_input:
            continue

        if user_input.lower() == "/quit":
            print("Fare thee well.")
            break
        if user_input.lower() == "/help":
            print_help()
            continue
        if user_input.lower() == "/clear":
            bot.clear_memory()
            print("\nMemory cleared.\n")
            continue
        if user_input.lower() == "/history":
            print_history(bot)
            continue

        try:
            reply = bot.ask(user_input)
            print(f"\nShakespeare: {reply}\n")
        except Exception as exc:
            print(f"\nError: {exc}\n")


if __name__ == "__main__":
    run_cli()
