"""
Per-user message history — tracks last N interactions for context awareness.
"""
from collections import defaultdict, deque
from datetime import datetime


class MessageHistory:
    """Maintains per-user conversation history (last N messages)."""

    def __init__(self, max_messages: int = 3):
        self.max_messages = max_messages
        self._history: dict[int, deque] = defaultdict(
            lambda: deque(maxlen=max_messages * 2)  # store both user + bot messages
        )

    def add_user_message(self, user_id: int, content: str):
        """Record a user message."""
        self._history[user_id].append({
            "role": "user",
            "content": content,
            "timestamp": datetime.now().isoformat(),
        })

    def add_bot_message(self, user_id: int, content: str):
        """Record a bot response."""
        self._history[user_id].append({
            "role": "assistant",
            "content": content,
            "timestamp": datetime.now().isoformat(),
        })

    def get_history(self, user_id: int) -> list[dict]:
        """
        Get the conversation history for a user.

        Returns:
            List of message dicts with role, content, timestamp.
        """
        return list(self._history[user_id])

    def get_summary_text(self, user_id: int) -> str:
        """Get a formatted text summary of recent interactions."""
        history = self.get_history(user_id)
        if not history:
            return "No recent interactions found."

        lines = []
        for msg in history:
            role = "🧑 You" if msg["role"] == "user" else "🤖 Bot"
            content = msg["content"]
            if len(content) > 200:
                content = content[:200] + "..."
            lines.append(f"{role}: {content}")

        return "\n".join(lines)

    def clear_history(self, user_id: int):
        """Clear history for a specific user."""
        if user_id in self._history:
            self._history[user_id].clear()
